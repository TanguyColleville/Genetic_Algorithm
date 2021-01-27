from RotTable import *
from Population import *
from Traj3D import * 
import random as rd 
rd.seed(0)
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
    iter_max=10
    
    Pop=Population("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG")
    Pop.evolve(iter_max)

def main_3():
    Pop=Population("AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG")
    Pop.next_gen()

if __name__ == "__main__" :
    main_2()


