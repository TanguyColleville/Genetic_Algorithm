from RotTable import *
from Population import *
from Traj3D import * 
import numpy as np
#np.random.seed(0)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", help="input filename of DNA sequence")
parser.parse_args()
args = parser.parse_args()

def main():

    rot_table = RotTable()
    traj = Traj3D()

    if args.filename:
	    # Read file
	    lineList = [line.rstrip('\n') for line in open("plasmid_8k.fasta")]
		# Formatting
	    seq = ''.join(lineList[1:])
	    traj.compute(seq, rot_table)
    else:
        traj.compute("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG", rot_table)
    print(traj.getTraj())

    if args.filename:
        traj.draw(args.filename+".png")
    else:
        traj.draw("sample.png")

def main_2():
    iter_max=30
    
    Pop=Population("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG")
    Pop.evolve(iter_max, "Tournoi")

def main_3():
    Pop=Population("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG")
    Pop.next_gen()

def test_draw_initial_seq(file_name):
    rot_table = RotTable()
    traj = Traj3D()
    lineList = [line.rstrip('\n') for line in open(file_name)]
    seq = ''.join(lineList[1:])
    traj.compute(seq, rot_table)
    print(traj.getTraj())
    traj.draw("sample.png")

def test_draw_traited(file_name,methode_sele,nbiter,nbindiv):
    lineList = [line.rstrip('\n') for line in open(file_name)]
    traj=Traj3D()
    seq = ''.join(lineList[1:])
    Pop=Population(seq,n=nbindiv)
    Pop.evolve(nbiter,methode_sele)
    traj.compute(seq,Pop._Get_Current_Best()[0])
    traj.draw("sample.png")

def main_4():
    lineList = [line.rstrip('\n') for line in open("./Data/plasmid_8k.fasta")]
    seq = ''.join(lineList[1:])
    pop_size = 100
    nb_gen = 20

    pop = Population(seq,pop_size)
    pop.evolve(nb_gen, "Tournoi", True, alpha=0.593879313130056)
    best = pop._Get_Current_Best()
    print("Meilleur score obtenu de",best[1],"avec l'individu :\n")
    print(best[0])

def draw_seq():
    rot_table = {'AA': [35.60831497330928, 7.300914398651058, -154.0], 'AC': [35.02399069084545, 2.666893442212051, 143.0], 'AG': [26.2, 8.994736694729562, 2.0], 'AT': [26.08456146107297, 7.648153845528422, 0.0], 'CC': [33.70967753141159, 0.9148954541563099, -57.0], 'CG': [30.820267576802113, 5.397768853723985, 0], 'GC': [39.355615833563824, 4.617189422112741, 180.0], 'TA': [35.93130323359519, -0.23199257503017134, 0.0], 'TC': [37.6615370686879, 10.949138895925273, -120.0], 'TG': [34.817713024996905, 82.349600699326, 64.0]}
    lineList = [line.rstrip('\n') for line in open("./Data/plasmid_8k.fasta")]
    seq = ''.join(lineList[1:])
    traj=Traj3D()
    traj.compute(seq,RotTable(rot_dict=rot_table).Reconstitution())
    traj.draw("sample.png")


if __name__ == "__main__" :
    #draw_seq()
    main_4()

