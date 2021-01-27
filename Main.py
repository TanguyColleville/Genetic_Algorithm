from RotTable import *
from Population import *
from Traj3D import * 
import numpy as np
np.random.seed(0)
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
    iter_max=100
    
    Pop=Population("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG")
    Pop.evolve(iter_max, "Elitisme")

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

if __name__ == "__main__" :
    main_2()


