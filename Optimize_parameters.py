import numpy as np
from scipy.optimize import minimize_scalar


from Population import Population


np.random.seed(1)


lineList = [line.rstrip('\n') for line in open("plasmid_8k.fasta")]
seq = ''.join(lineList[1:])
pop_size = 1000
nb_gen = 20


def best_score_given_mutation_probability(alpha):
    """permet d'effectuer une optimisation sur la probabilité de mutation d'un individu"""
    pop = Population(seq, pop_size)
    pop.evolve(nb_gen, "Tournoi", alpha=alpha)
    return pop._Get_Current_Best()[1]


# Problème d'optimisation sous contrainte : 0<=alpha<=1 car c'est une
# probabilité et minimisation de la fonction coût
res = minimize_scalar(
    best_score_given_mutation_probability, bounds=(
        0, 1), method='bounded')

if res.success:
    print("Minimum trouvé !\n")
    print("Valeur minimale obtenue de", res.fun, "pour alpha =", res.x)
else:
    print("Pas de minimum trouvé...")
