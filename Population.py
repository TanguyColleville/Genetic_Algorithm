# import RotTable.RotTable
from RotTable import RotTable
from Traj3D import *
import mathutils
from operator import itemgetter, attrgetter
import pickle

class Population():
    """Represents the population of rotation tables (individuals)"""

    def __init__(self, seq,n=10):
        if type(n) is not int or n<3:
            raise Exception(" n must be an integer greater than 2")
        if type(seq) is not str :
            raise Exception(" seq must be a string which represents dinucleotides")
        self._pop = []  # Liste d'invididus i.e. [rot_table, score]
        self._current_gen = 0 # Génération courante
        self._seq = seq  # Séquence à l'étude
        self._current_best_index = 0 # Meilleur score à la génération courante
        for e in range(n):
            self.add_to_pop(RotTable(randomGen=True), None) # On ajoute à la population un individu généré aléatoirement avec un score à None par défaut
        
        traj_ini = Traj3D()
        traj_ini.compute(seq, RotTable().Reconstitution()) # On calcule la trajectoire
        extremite_1_ini = traj_ini.getTraj()[0]
        extremite_2_ini = traj_ini.getTraj()[-1]
        self._iniD = (extremite_2_ini-extremite_1_ini).length


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
        return None if self._current_best_index is None else self._pop[self._current_best_index]

    def _Get_Current_Best_Index(self):
        return self._current_best_index
    
    def _Get_iniD(self):
        return self._iniD
    #################
    # MODIFICATEURS #
    ################# 

    def add_to_pop(self, individual, score=None):
        self._pop.append([individual, score])

    def del_from_pop(self,rang):
        if not type(rang)==int and rang in range(len(self._pop)): 
            raise Exception("Rang must be an int")
        del(self._pop[rang])

    def update_current_gen(self):
        self._current_gen += 1
        
    def set_pop(self,liste):
        if not type(liste)==list:
            raise Exception("Liste must be a list type")
        self._pop=liste[:]

    def clear_pop(self):
        self.set_pop([])

    def update_current_best_index(self, new_best_index):
        self._current_best_index = new_best_index
    
    ########################
    # FONCTIONS EVOLUTIVES #
    ########################
    
    def eval_pop_scaling(self, N):
        ''' Modifie la fonction d'évaluation avec du scaling pour moins converger localement, en particulier au début
        Nécessite N le nombre de génération total prévu '''
        if not type(N)==int :
            raise Exception("N must be an int")
        p = 0.1
        n = self._current_gen
        if n==0:
            k = (np.tan((n+1/(N+1))*np.pi/2))**p
        else:
            k = (np.tan((n/(N+1))*np.pi/2))**p
        # k commence proche de 0 donc lisse les scores, puis augmente en passant par 1 ;
        # plus N est grand, plus k augmente, à terme ; pour N à 1000000, k vaut environ 3 à la dernière génération
        for individu in self._pop:
            individu[1] = (individu[0].Evaluation(self._seq, self._iniD))**k


    def eval_pop(self):
        ''' Attribue un score à chaque individu de la population '''
        current_best_score = math.inf
        best_indiv_index = 0
        for i in range(len(self._pop)): # On parcourt la population...
            score = self._pop[i][0].Evaluation(self._seq, self._iniD)
            if score < current_best_score:
                best_indiv_index = i
                current_best_score = score
            self._pop[i][1]=score # ...et on affecte à chaque individu son nouveau score
        self.update_current_best_index(best_indiv_index)
    
    def select_elite_pop(self,coefficient = 0.5):
        '''Fonction de sélection par élitisme de la population : ne garde que les "coefficient%" individus de score le plus bas'''
        if (not type(coefficient)==float) and (coefficient>1 or coefficient<0):
            raise Exception("coefficient must be a float between 0 and 1 ")
        L = sorted(self._pop, key=itemgetter(1)) # On récupère la liste de la population triée par scores
        n = len(self._pop)
        self.clear_pop() # On efface l'ancienne population
        for i in range(1,int(n*coefficient)) : # Et on rajoute les n*coefficients premiers/meilleurs
            self._pop.append(L[i])
        self._pop.append(L[0])
        self.update_current_best_index(len(self._pop)-1)

    def select_tournoi_pop(self, luck_prob, puissance):
        '''Fonction de sélection par tournoi de la population ; il y a une probabilité que le plus faible des combattants 
        (plus haut score) gagne quand même : proba ; celle-ci dépend de la différence de score entre les deux combattants
        et on peut ajouter un paramètre luck_prob qui pondère cette probabilité ; à noter que le meilleur individu est
        exempt de cette probabilité pour être certain qu'il n'est pas éliminé.
        
        Par défaut, luck_prob = 0 et puissance = 2, cf evolve. '''
        if not type(luck_prob)==float and (luck_prob>1 or luck_prob<0) : 
            raise Exception("Luck_prob should be a float value between 0 and 1")
        if not type(puissance)==int : 
            raise Exception("Puissance should be an integer")
        best_individu = self._pop.pop(self._current_best_index)
        L = [] # Tableau des vainqueurs
        n = len(self._pop)  # Taille de la population
        remaining = [i for i in range(n)] # Liste des indices des individus n'ayant pas encore combattu
        while n>1:
            i1 = np.random.randint(0,n) # On tire un 1er nombre au hasard...
            j1 = remaining.pop(i1) # ...qui nous donne l'indice d'un individu à faire combattre
            i2 = np.random.randint(0,n-1) # On tire un 2e nombre au hasard...
            j2 = remaining.pop(i2) # ...qui nous donnent l'indice d'un autre individu à faire combattre
            score1 = self._pop[j1][1]
            score2 = self._pop[j2][1]
            diff = score1 - score2
            if diff < 0:
                proba = (1 - (-diff/score2)**puissance)*luck_prob
                if np.random.random()<proba:
                    L.append(self._pop[j2])
                else:
                    L.append(self._pop[j1])
            else:
                proba = (1 - (diff/score1)**puissance)*luck_prob
                if np.random.random()<proba:
                    L.append(self._pop[j1])
                else:
                    L.append(self._pop[j2])
            #L.append(self._pop[j1 if self._pop[j1][1]<self._pop[j2][1] else j2]) # On ajoute alors à L l'individu vainqueur du combat
            n -= 2
        self.clear_pop() # On vide l'ancienne population
        for individu in L: # Et on rajoute tous les vainqueurs
            self._pop.append(individu)
        self._pop.append(best_individu)
        self.update_current_best_index(len(self._pop)-1)


    def cross_pop(self): 
        '''Fonction de croisement de la population : double sa taille'''
        
        l = len(self._pop)
        if l%2 == 1: # Si il y a un nombre impair d'individus, on en prélève un (mais pas le meilleur)
            best_individu = (self._pop).pop()
            extra_individu = (self._pop).pop()
            self._pop.append(best_individu)
            self.update_current_best_index(len(self._pop)-1)

        for i in range(0, len(self._pop)-l%2, 2): # On parcourt la population...
            cut = np.random.randint(0, RotTable._RotTable__NUM_KEYS) # ...on tire un indice de coupe au hasard...
            cross_1, cross_2 = self._pop[i][0].Cross(self._pop[i+1][0],cut) # ...et on effectue le croisement
            self.add_to_pop(cross_1) # ...on ajoute enfin les 2 enfants du croisement
            self.add_to_pop(cross_2)

        if l%2 == 1: self._pop.append(extra_individu) # Si il y avait un nombre impair d'individus, on rajoute l'individu prélevé initialement
    
    def mutate_pop(self, alpha):
        ''' Mutation de tous les individus composant notre population avec une probabilité alpha (par défaut 0.01 tel que 
        déterminé dans evolve) SAUF le meilleur individu qui n'est jamais muté si cette mutation est a posteriori 
        dégradante. '''
        if not type(alpha)==float and (alpha>1 or alpha<0) : 
            raise Exception("alpha should be a float value between 0 and 1")
        best = self._pop.pop() # On prélève le meilleur
        mutate_best = RotTable(rot_dict=best[0].getRotTable().copy()) # et on le duplique
        mutate_best.Mutate(self._current_gen) # On fait muter la copie du meilleur (de manière certaine)
        mutate_best_eval = mutate_best.Evaluation(self._seq, self._iniD) # et on calcule son score

        n = len(self._pop)
        k = np.random.binomial(n, alpha) # On génère le nombre d'individus à muter...
        individuals_to_mutate = np.random.randint(0,n,k) # ...et on en génère autant d'indices

        for i in individuals_to_mutate: # On parcourt les indices des individus à muter...
            self._pop[i][0].Mutate(self._current_gen) # ...et on fait muter chaque individu correspondant

        if mutate_best_eval < best[1]: # Si la mutation du meilleur est encore meilleure...
            self._pop.append([mutate_best,mutate_best_eval]) # ...on l'ajoute à la population
        else:
            self._pop.append(best) # Sinon on rajoute le meilleur 
        self.update_current_best_index(len(self._pop)-1)

    ############################
    # ITERATION DE GENERATIONS #
    ############################ 

    def next_gen(self, n, scaling, selection_method, alpha, luck_prob, puissance):
        ''' Passage à la génération suivante : une itération de la boucle évaluation, sélection, croisement, mutation
        On peut choisir 
        - la méthode de sélection choisie entre tournoi et élitisme avec selection_method = "Tournoi" par défaut
        - l'évaluation avec ou sans scaling avec le paramètre scaling = False par défaut
        - le paramètre alpha =  0.01 par défaut qui correspond au taux de mutation (chance qu'une mutation ait lieu par génération)
        On trouve également les luck_prob et puissance associés à la sélection par tournoi, et n le nombre de générations
        étudié, nécessaire pour calculer l'évaluation avec scaling. '''
        if not type(n)==int : 
            raise Exception("n should be an integer")
        # print(type(scaling))
        if not (scaling==True or scaling==False): 
            raise Exception("scaling should be a boolean")
        # les types des autres variables sont tester dans l'entrée des autres méthodes

        if scaling:
            self.eval_pop_scaling(n)
        else:
            self.eval_pop()
        if selection_method == "Elitisme":
            self.select_elite_pop()
        elif selection_method == "Tournoi":
            self.select_tournoi_pop(luck_prob, puissance)
        else:
            raise Exception(" selection_method must be either 'Elitisme' or 'Tournoi'")
        print(self._pop[self._current_best_index][1],self._pop[self._current_best_index][0],'\n')
        print(self._pop[-2][1],self._pop[-1][0],'\n')
        print(self._pop[-3][1],self._pop[-2][0],'\n\n')
        self.mutate_pop(alpha)
        print(self._pop[self._current_best_index][1],self._pop[self._current_best_index][0],'\n')
        print(self._pop[-2][1],self._pop[-1][0],'\n')
        print(self._pop[-3][1],self._pop[-2][0],'\n\n\n\n\n')
        self.cross_pop()
        self.update_current_gen()

    def evolve(self, n, scaling = False, selection_method = "Tournoi", alpha=0.59, luck_prob=0, puissance=2):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération. Ce sont ses paramètres qui déterminent ceux de toutes
        les autres fonctions évolutionnaires utilisées car c'est la fonction qu'on appelle dans main.'''

        for i in range(n-1): # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(n, scaling, selection_method, alpha, luck_prob, puissance)
        self.eval_pop() # pour avoir une population dont tous les individus ont un score

    def evolve_verbose(self, n, scaling = False, selection_method = "Tournoi", alpha=0.59, luck_prob=0, puissance=2):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération. Ce sont ses paramètres qui déterminent ceux de toutes
        les autres fonctions évolutionnaires utilisées car c'est la fonction qu'on appelle dans main.'''
        print(type(scaling))
        for i in range(n-1): # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(n, scaling, selection_method, alpha, luck_prob, puissance)
            print(self._current_best_index)
            print(self._pop)
        pickle.dump(self, open("Output/pop_avant_eval.p", "wb"))
        self.eval_pop() # pour avoir une population dont tous les individus ont un score
        pickle.dump(self, open("Output/pop_apres_eval.p", "wb"))
        print(self._current_best_index)
        print(self._pop)
    
    def evolve_with_step(self, n, step, scaling = False, alpha=0.59,  selection_method = "Tournoi", luck_prob=0, puissance=2):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération. Ce sont ses paramètres qui déterminent ceux de toutes
        les autres fonctions évolutionnaires utilisées car c'est la fonction qu'on appelle dans main.'''
        C = []
        for i in range(n-1): # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(n, scaling, selection_method, alpha, luck_prob, puissance)
            if i%step==0:
                C.append(self._pop[self._current_best_index][1])
        self.eval_pop() # pour avoir une population dont tous les individus ont un score
        if (n-1)%step==0:
                C.append(self._pop[self._current_best_index][1])
        return C

    def evolve_and_graph(self, n, scaling = False, alpha=0.59,  selection_method = "Tournoi", luck_prob=0, puissance=2):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération '''
        x = []
        y = []
        for i in range(n-1): # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(n, scaling, selection_method, alpha, luck_prob, puissance)
            new_y = self._pop[self._current_best_index][1]
            y.append(new_y)
            x.append(self._current_gen)
            print("Le meilleur individu a un score de :", new_y, "\n")
        self.eval_pop() # pour avoir une population dont tous les individus ont un score
        print("Dernière génération :", self._current_gen)
        print("Le meilleur individu a un score de :", self._pop[self._current_best_index][1], "\n")
        y.append(self._pop[self._current_best_index][1])
        x.append(self._current_gen + 1 )
        fig, ax = plt.subplots()
        plt.xlabel('Nombre de générations')
        plt.ylabel('Meilleur score')
        plt.title('Evolution du meilleur score de la population au fil des générations')
        plt.plot(x,y,'ro--')
        plt.savefig("Output/Convergence{}_{}_{}_{}_{}.png".format(n,scaling,selection_method,luck_prob,puissance))
        plt.show()
 

            
            
            