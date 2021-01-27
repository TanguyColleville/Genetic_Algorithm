# import RotTable.RotTable
from RotTable import RotTable
from Traj3D import *
import mathutils
from operator import itemgetter, attrgetter


class Population():
    """Represents the population of rotation tables (individuals)"""

    def __init__(self, seq,n=5):
        if type(n) is not int or n<2:
            raise Exception(" n must be an integer greater than 1")
        if type(seq) is not str : 
            raise Exception(" seq must be a string which represents dinucleotides")
        self._pop = []  # Liste d'invididus i.e. [rot_table, score]
        self._current_gen = 0 # Génération courante
        self._seq = seq  # Séquence à l'étude
        self._current_best = None # Meilleur score à la génération courante
        for e in range(n):
            self.add_to_pop(RotTable(randomGen=True), None) # On ajoute à la population un individu généré aléatoirement avec un score à None par défaut
    
    ##############
    # ASSESSEURS #
    ############## 
    
    def _Get_pop(self):  
        return self._pop
    
    def _Get_seq(self):
        return self._seq
    
    def _Get_len(self):
        return len(self._pop)

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
        self._current_gen += 1
        
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

        for individu in self._pop: # On parcourt la population...
            individu[1]=individu[0].Evaluation(self._seq) # ...et on affecte à chaque individu son nouveau score

    
    def select_elite_pop(self,coefficient = 0.5):
        '''Fonction de sélection par élitisme de la population : ne garde que les "coefficient%" individus de score le plus bas'''
        
        L = sorted(self._pop, key=itemgetter(1)) # On récupère la liste de la population triée par scores
        n = len(self._pop)
        self.clear_pop() # On efface l'ancienne population
        for i in range(int(n*coefficient)) : # Et on rajoute les n*coefficients premiers/meilleurs
            self._pop.append(L[i])
        self.update_current_best(self._pop[0][1]) # Enfin on met à jour le meilleur score

    def select_tournoi_pop(self):
        '''Fonction de sélection par tournoi de la population'''
        L = [] # Tableau des vainqueurs
        n = len(self._pop) # Taille de la population
        remaining = [i for i in range(n)] # Liste des indices des individus n'ayant pas encore combattu
        while n>1:
            i1 = np.random.randint(0,n) # On tire un 1er nombre au hasard...
            j1 = remaining.pop(i1) # ...qui nous donne l'indice d'un individu à faire combattre
            i2 = np.random.randint(0,n-1) # On tire un 2e nombre au hasard...
            j2 = remaining.pop(i2) # ...qui nous donnent l'indice d'un autre individus à faire combattre
            L.append(self._pop[j1 if self._pop[j1][1]<self._pop[j2][1] else j2]) # On ajoute alors à L l'individu vainqueur du combat
            n -= 2
        self.clear_pop() # On vide l'ancienne population
        for individu in L: # Et on rajoute tous les vainqueurs
            self._pop.append(individu)
        self.update_current_best(min(L,key=itemgetter(1))[1]) # On met à jour le meilleur score


    def cross_pop(self): 
        '''Fonction de croisement de la population : double sa taille'''
        
        l = len(self._pop)
        if l%2 == 1: extra = (self._pop).pop() # Si il y a un nombre impair d'individus, on en prélève un

        for i in range(0, len(self._pop)-l%2, 2): # On parcourt la population...
            cut = np.random.randint(0, 16) # ...on tire un indice de coupe au hasard...
            cross_1, cross_2 = self._pop[i][0].Cross(self._pop[i+1][0],cut) # ...et on effectue le croisement
            self.add_to_pop(cross_1) # ...on ajoute enfin les 2 enfants du croisement
            self.add_to_pop(cross_2)

        if l%2 == 1: self.add_to_pop(extra[0]) # Si il y avait un nombre impair d'individus, on rajoute l'individu prélever initialement

    
    def mutate_pop(self):
        ''' Mutation de tous les individus composant notre population '''

        for indiv in self._pop: # On parcourt la population...
            indiv[0].Mutate(self._current_gen) # ...et on fait muter chaque individu (avec une certaine probabilité, cf méthode Mutate de la classe RotTable)

    ############################
    # ITERATION DE GENERATIONS #
    ############################ 

    def next_gen(self):
        ''' Passage à la génération suivante : une itération de la boucle évaluation, sélection, croisement, mutation'''

        self.eval_pop()
        self.select_tournoi_pop()
        self.cross_pop()
        self.mutate_pop()
        self.update_current_gen()

    def evolve(self,n):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération '''
        
        for i in range(n-1): # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen()
            print("Le meilleur individu a un score de :", self._current_best, "\n")
        self.eval_pop() # pour avoir une population dont tous les individus ont un score
        print("Dernière génération :", self._current_gen)
        print("Le meilleur individu a un score de :", self._current_best, "\n")
 

            
            
            