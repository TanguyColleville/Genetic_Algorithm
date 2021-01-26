import mathutils
import math
import numpy as np
from Traj3D import *


class RotTable:
    """Represents the rotation table"""

    __KEYS = ["AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT"]

    __ORIGINAL_ROT_TABLE = {
        "AA": [35.62, 7.2, -154, 0.06, 0.6, 0],
        "AC": [34.4, 1.1, 143, 1.3, 5, 0],
        "AG": [27.7, 8.4, 2, 1.5, 3, 0],
        "AT": [31.5, 2.6, 0, 1.1, 2, 0],
        "CA": [34.5, 3.5, -64, 0.9, 34, 0],
        "CC": [33.67, 2.1, -57, 0.07, 2.1, 0],
        "CG": [29.8, 6.7, 0, 1.1, 1.5, 0],
        "CT": [27.7, 8.4, -2, 1.5, 3, 0],
        "GA": [36.9, 5.3, 120, 0.9, 6, 0],
        "GC": [40, 5, 180, 1.2, 1.275, 0],
        "GG": [33.67, 2.1, 57, 0.07, 2.1, 0],
        "GT": [34.4, 1.1, -143, 1.3, 5, 0],
        "TA": [36, 0.9, 0, 1.1, 2, 0],
        "TC": [36.9, 5.3, -120, 0.9, 6, 0],
        "TG": [34.5, 3.5, 64, 0.9, 34, 0],
        "TT": [35.62, 7.2, 154, 0.06, 0.6, 0]
    }

    def __init__(self, randomGen=False, rot_dict=None):
        if rot_dict is None:
            self.__Rot_Table = {}
            for dinucleotide in RotTable.__ORIGINAL_ROT_TABLE:
                self.__Rot_Table[dinucleotide] = RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][:3]
            if randomGen:
                for dinucleotide in RotTable.__ORIGINAL_ROT_TABLE:
                    self.__Rot_Table[dinucleotide] = np.random.randint(
                        -180, 180)*np.random.randn(3)
        else:
            self.__Rot_Table = rot_dict

    ###################
    # READING METHODS #
    ###################
    def __str__(self):
        return "{}".format(self.__Rot_Table)
    
    def getTwist(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][0]

    def getWedge(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][1]

    def getDirection(self, dinucleotide):
        return self.__Rot_Table[dinucleotide][2]

    def getRotTable(self):
        return self.__Rot_Table

    ###################
    # WRITING METHODS #
    ###################
    
    def Encodage(self):
        pass
    
    def Mutate(self):
        pass
    
    def Evaluation(self, seq):
        traj = Traj3D()
        traj.compute(seq, self) # On calcule la trajectoire
        extremite_1 = traj.getTraj()[0]
        extremite_2 = traj.getTraj()[-1]
        return (extremite_2-extremite_1).length # On retourne le score

    ###################
