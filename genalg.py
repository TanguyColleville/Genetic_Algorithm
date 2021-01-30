import argparse


import pickle


from Population import Population
from RotTable import RotTable
from Traj3D import Traj3D

# création des arguments pour utilisation du produit via un terminal python

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    type=str,
    choices=[
        'evolution',
        'display'],
    help="Working mode of the program")
parser.add_argument(
    "DNA_sequence",
    type=str,
    help="Filename of the DNA sequence to work with")
parser.add_argument(
    "-ni",
    "--number_of_individuals",
    type=int,
    default=10,
    help="Number of individuals in the initial population")
parser.add_argument(
    "-ng",
    "--number_of_generation",
    type=int,
    default=5,
    help="Number of generations to go through")
parser.add_argument(
    "-sel",
    "--selection_method",
    type=str,
    choices=[
        'Elitisme',
        'Tournoi'],
    default='Tournoi',
    help="Selection method to be used by the algorithm")
parser.add_argument(
    "--scaling",
    action="store_true",
    help="Specify in order to use evaluation with scaling")
parser.add_argument(
    "-a",
    "--alpha",
    type=float,
    default=0.59,
    help="Probability of mutation for each individual")
parser.add_argument(
    "-l",
    "--luck",
    type=float,
    default=0.7,
    help="Only relevent when using 'Tournoi' selection. Used to weight the probability of a loser being selected.")
parser.add_argument(
    "-p",
    "--power",
    type=int,
    default=2,
    help="Only relevent when using 'Tournoi' selection. Increasing this number will lead in increased influence of the luck (-l) parameter in the calculation that determines the probability of a loser being selected.")
parser.add_argument(
    "-s",
    "--save",
    type=str,
    help="File location to save the best individual's RotTable dictionary")
parser.add_argument(
    "--load",
    type=str,
    help="File location of a RotTable's dictionary to display a DNA sequence")
parser.parse_args()
args = parser.parse_args()


def make_evolution(seq, N_gen, N_ind, sel, scaling, alpha, luck, p):
    """lance l'évolution de la population"""
    pop = Population(seq, N_ind)
    pop.evolve(
        N_gen,
        selection_method=sel,
        scaling=scaling,
        alpha=alpha,
        luck_prob=luck,
        puissance=p)
    return pop._Get_Current_Best()


def display_seq_from_file(seq, rot_table_file):
    """Trace le brin d'ADN en 3D à partir du fichier en question et de la table par défaut"""
    if rot_table_file is None:
        rot_table_object = RotTable()
    else:
        rot_table_object = RotTable(
            rot_dict=pickle.load(
                open(
                    rot_table_file,
                    "rb")))
    traj = Traj3D()
    traj.compute(seq, rot_table_object.Reconstitution())
    traj.draw("sample.png")


def display_seq_from_object(seq, rot_table):
    """ Trace le brin d'ADN à partir de la table des angles optimisés"""
    traj = Traj3D()
    traj.compute(seq, rot_table.Reconstitution())
    traj.draw("sample.png")


lineList = [line.rstrip('\n') for line in open(args.DNA_sequence)]
seq = ''.join(lineList[1:])

if args.mode == 'evolution':
    best = make_evolution(
        seq,
        args.number_of_individuals,
        args.number_of_generation,
        args.selection_method,
        args.scaling,
        args.alpha,
        args.luck,
        args.power)
    print("Meilleur score obtenu de", best[1], "avec l'individu :\n")
    print(best[0])
    if args.save:
        pickle.dump(best[0].getRotTable(), open(args.save, "wb"))
    display_seq_from_object(seq, best[0])
elif args.mode == 'display':
    display_seq_from_file(seq, args.load)
else:
    raise Exception("mode should be either 'evolution' or 'display'")
