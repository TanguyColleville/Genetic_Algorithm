# import RotTable.RotTable
from RotTable import RotTable
from Traj3D import *
import mathutils
from operator import itemgetter, attrgetter


class Population():
    """Represents the population of rotation tables (individuals)"""

    def __init__(self, seq,n=5):
        self._pop = []  # Liste de couple d'invididus i.e. RotTable avec leurs scores
        self._current_gen = 0 # génération de la population à l'année 0
        self._seq = seq  # Séquence à l'étude
        self._current_best = 0
        for e in range(n):
            self.add_to_pop(RotTable(randomGen=True), None) # on ajoute un individu à la population avec un score nul par défaut
    
    ##############
    # ASSESSEURS #
    ############## 
    
    def _Get_pop(self):  
        return self._pop
    
    def _Get_seq(self):
        return self._seq
    
    def _Get_len(self):
        return len(self._Get_pop())

    def _Get_Current_Gen(self):
        return self._current_gen
    
    def _Get_Current_Best(self):
        return self._current_best
    
    #################
    # MODIFICATEURS #
    ################# 

    def add_to_pop(self, individual, score=None):
        self._pop.append([individual, score])

    def del_from_pop(self,rang):
        del(self._pop[rang])

    def update_current_gen(self):
        self._current_gen +=1
        
    def set_pop(self,liste):
        self._pop=liste[:]

    def clear_pop(self):
        self.set_pop([])

    def update_current_best(self, new_best):
        self._current_best = new_best
    
    ########################
    # FONCTIONS EVOLUTIVES #
    ######################## 

    def eval_pop(self):
        ''' Attribue un score à chaque individu de la population '''

        for individu in self._Get_pop():
            individu[1]=individu[0].Evaluation(self._Get_seq())

    
    def select_pop(self,coefficient):
        '''Fonction de sélection par élitisme de la population : ne garde que les "coefficient%" individus de score le plus bas'''
        
        L = sorted(self._Get_pop(), key=itemgetter(1))
        n = self._Get_len()
        self.clear_pop()
        for i in range(int(n*(1-coefficient))) :
            self._Get_pop().append(L[i])
        self.update_current_best(self._Get_pop()[0][1])


    def cross_pop(self): 
        '''Fonction de croisement de la population : double sa taille'''
        
        l = self._Get_len()
        if l%2 == 1:
            extra = (self._Get_pop()).pop()
            for i in range(0, self._Get_len()-1, 2): #pas de deux, problème de parité d'où extra
                cut = np.random.randint(0, 16)
                child1 = {}
                child2 = {}
                keys = RotTable._RotTable__KEYS
                #keys = ["AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT"]
                for j in keys[:cut]:
                    child1[j] = self._Get_pop()[i][0].getRotTable()[j]
                    child2[j] = self._Get_pop()[i+1][0].getRotTable()[j]
                for j in keys[cut:]:
                    child1[j] = self._Get_pop()[i][0].getRotTable()[j]
                    child2[j] = self._Get_pop()[i+1][0].getRotTable()[j]
                self.add_to_pop(RotTable(child1))
                self.add_to_pop(RotTable(child2))
            self.add_to_pop(extra)
        else:
            for i in range(0, self._Get_len(), 2): #pas de deux, problème de parité d'où extra
                cut = np.random.randint(0, 16)
                child1 = {}
                child2 = {}
                keys = RotTable._RotTable__KEYS
                #keys = ["AA","AC","AG","AT","CA","CC","CG","CT","GA","GC","GG","GT","TA","TC","TG","TT"]
                for j in keys[:cut]:
                    child1[j] = self._Get_pop()[i][0].getRotTable()[j]
                    child2[j] = self._Get_pop()[i+1][0].getRotTable()[j]
                for j in keys[cut:]:
                    child1[j] = self._Get_pop()[i][0].getRotTable()[j]
                    child2[j] = self._Get_pop()[i+1][0].getRotTable()[j]
                self.add_to_pop(RotTable(child1))
                self.add_to_pop(RotTable(child2))

    
    def mutate_pop(self):
        ''' Mutation de tous les individus composants notre population '''

        for indiv in self._Get_pop():
            indiv[0].Mutate()

    ############################
    # ITERATION DE GENERATIONS #
    ############################ 

    def next_gen(self):
        ''' Passage à la génération suivante '''

        self.eval_pop()
        self.select_pop(0.5)
        self.cross_pop()
        self.mutate_pop()
        self.update_current_gen()

    def evolve(self,n):
        for i in range(n):
            self.next_gen()
            print("Génération :", self._Get_Current_Gen())
            print("Le meilleur individu a un score de :", self._Get_Current_Best(), "\n")

 
            
            
            