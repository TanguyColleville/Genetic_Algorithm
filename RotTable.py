import mathutils
import math
import numpy as np
from Traj3D import *


class RotTable:
    """Represents the rotation table"""

    __KEYS = ["AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT"]

    __NUM_KEYS = 10

    __KEYS_UNIQUE = ["AA","AC","AG","AT","TA","TC","TG","CC","CG","GC"]

    __ORIGINAL_ROT_TABLE = {
        "AA": [35.62, 7.2, -154, 0.06, 0.6, 0],
        "AC": [34.4, 1.1, 143, 1.3, 5, 0],
        "AG": [27.7, 8.4, 2, 1.5, 3, 0],
        "AT": [31.5, 2.6, 0, 1.1, 2, 0],
        "CC": [33.67, 2.1, -57, 0.07, 2.1, 0],
        "CG": [29.8, 6.7, 0, 1.1, 1.5, 0],
        "GC": [40, 5, 180, 1.2, 1.275, 0],
        "TA": [36, 0.9, 0, 1.1, 2, 0],
        "TC": [36.9, 5.3, -120, 0.9, 6, 0],
        "TG": [34.5, 3.5, 64, 0.9, 34, 0],
    }
    
    __BORNES = {
        'AA': [[35.56, 35.68], [6.65, 7.8]],
        'AC': [[33.1, 35.7], [-3.9, 6.1]], 
        'AG': [[26.2, 29.2], [5.4, 11.4]], 
        'AT': [[30.4, 32.6], [0.6, 4.6]], 
        'CC': [[33.6, 33.74], [0.0, 4.2]], 
        'CG': [[28.7, 30.9], [5.2, 8.2]], 
        'GC': [[38.8, 41.2], [3.725, 6.275]], 
        'TA': [[34.9, 37.1], [-1.1, 2.9]], 
        'TC': [[36.0, 37.8], [-0.7, 11.3]], 
        'TG': [[33.6, 35.4], [-30.5, 37.5]]}

    def __init__(self, randomGen=False, rot_dict=None):
        if rot_dict is None:
            self.__Rot_Table = {}
            for dinucleotide in RotTable.__ORIGINAL_ROT_TABLE:
                self.__Rot_Table[dinucleotide] = []
                for i in range(3):
                    self.__Rot_Table[dinucleotide].append(RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][i])
                    self.__Rot_Table[dinucleotide][i] += np.random.uniform(-1,1)*RotTable.__ORIGINAL_ROT_TABLE[dinucleotide][i+3] if randomGen else 0 ### on initialise en ajoutant une valeur alétoire avec une loi qui respecte les contraintes d'intervalles
        else:
            if type(rot_dict)==dict :
                self.__Rot_Table = rot_dict
            else : 
                raise Exception("Type of rot_dict is not correct, you should give a dictionnary")
        
    ###################
    # READING METHODS #
    ###################
    def __str__(self):
        return "{}".format(self.__Rot_Table)
    
    def getTwist(self, dinucleotide):
        return self.Reconstitution().getRotTable()[dinucleotide][0]

    def getWedge(self, dinucleotide):
        return self.Reconstitution().getRotTable()[dinucleotide][1]

    def getDirection(self, dinucleotide):
        return self.Reconstitution().getRotTable()[dinucleotide][2]

    def getRotTable(self):
        return self.__Rot_Table

    ###################
    # WRITING METHODS #
    ###################
    
    def Correspondance(self, nucle):
        ''' Associe à chaque nucléotide son symétrique : A et T, C et G '''
        if nucle == 'A':
            return 'T'
        elif nucle == 'T':
            return 'A'
        elif nucle == 'C':
            return 'G'
        elif nucle == 'G':
            return 'C'
    
    def Symetrique(self, dinucle):
        ''' Associe à chaque dinucléotide son symétrique grâce à Correspondace '''
        sym = ''
        sym += self.Correspondance(dinucle[1])
        sym += self.Correspondance(dinucle[0])
        return sym


    def Reconstitution(self):
        ''' Permet de reconstituer la table de rotation complète par symétrie, le temps d'évaluer l'individu '''
        table = self.__Rot_Table.copy()
        for dinucle in self.__KEYS_UNIQUE:
            if self.Symetrique(dinucle) not in self.__Rot_Table.keys():
                table[self.Symetrique(dinucle)] = []
                for i in range(len(table[dinucle])):
                    if i != 2:
                        table[self.Symetrique(dinucle)].append(table[dinucle][i])
                    else:
                        table[self.Symetrique(dinucle)].append(-table[dinucle][i])
        return RotTable(rot_dict=table)

                    
    
    def Mutate(self, gen):
        if not (type(gen) is int):
            raise Exception("gen must be an integer which represents the current generation")
        dinucle = np.random.choice(list(self.__Rot_Table.keys()))
        angle = np.random.randint(0,2) # on modifie un angle au hasard parmi ceux qu'on peut modifier (que deux choix)
        delta = self.__ORIGINAL_ROT_TABLE[dinucle][angle+3] # on récupère la variance de l'angle 
        #moyenne = self.__ORIGINAL_ROT_TABLE[dinucle][angle] # on récupère la valeur moyenne de l'angle 

        var = np.random.normal(0,10)*delta/math.log(gen+10) # réduire l'écart type au fil des générations
        if np.random.choice([True, False]):
            future = self.__Rot_Table[dinucle][angle] - var
            #borne = moyenne - delta
            borne = self.__BORNES[dinucle][angle][0]
            self.__Rot_Table[dinucle][angle] = future if future > borne else borne
        else:
            future = self.__Rot_Table[dinucle][angle] + var
            #borne = moyenne + delta
            borne = self.__BORNES[dinucle][angle][1]
            self.__Rot_Table[dinucle][angle] = future if future < borne else borne
            
    
    def Evaluation1(self,seq, ini_D):
        if type(seq) is not str : 
            raise Exception(" seq must be a string which represents dinucleotides")
        traj = Traj3D()
        traj.compute(seq, self.Reconstitution()) # On calcule la trajectoire
        extremite_1 = traj.getTraj()[0]
        extremite_2 = traj.getTraj()[-1]

        norme_1=(sum([extremite_1[i]**2 for i in range(len(extremite_1))]))**0.5
        norme_2=(sum([extremite_2[i]**2 for i in range(len(extremite_2))]))**0.5
        norme1_norme2=norme_1*norme_2
        ps_1_2=sum([x * y for x, y in zip(extremite_1, extremite_2)])
        costheta=abs(ps_1_2/norme1_norme2)
        distance=(extremite_2-extremite_1).length
        return (1-abs(costheta)+distance/ini_D)*1000

    def Evaluation(self,seq, ini_D):
        if type(seq) is not str : 
            raise Exception(" seq must be a string which represents dinucleotides")
        traj = Traj3D()
        traj.compute(seq, self.Reconstitution()) # On calcule la trajectoire
        extremite_1 = traj.getTraj()[0]
        extremite_2 = traj.getTraj()[-1]
        return (extremite_2 - extremite_1).length

    def Cross(self, rot_table_2, cut):
        '''Fonction de croisement de 2 individus'''
        if not isinstance(rot_table_2, RotTable): 
            raise Exception("rot_table_2 should be a RotTable instance")
        
        if not (type(cut) is int and cut in range(self.__NUM_KEYS)):
            raise Exception("cut should be an integer and between 0 and 16")
        child1 = {}
        child2 = {}
        keys = self.__KEYS_UNIQUE
        for j in keys[:cut]:
            child1[j] = self.getRotTable()[j].copy()
            child2[j] = rot_table_2.getRotTable()[j].copy()
        for j in keys[cut:]:
            child1[j] = self.getRotTable()[j].copy()
            child2[j] = rot_table_2.getRotTable()[j].copy()
        return (RotTable(child1),RotTable(child2))

    ###################
