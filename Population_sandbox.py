from operator import itemgetter
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

import pickle
from datetime import datetime


from RotTable import RotTable
from Traj3D import *
import copy


class Population_sandbox():
    """Represents the population of rotation tables (individuals)"""

    def __init__(self, seq, n=10):
        if not isinstance(n, int) or n < 3:
            raise Exception(" n must be an integer greater than 2")
        if not isinstance(seq, str):
            raise Exception(
                " seq must be a string which represents dinucleotides")
        self._pop = []  # Liste d'invididus i.e. [rot_table, score]
        self._current_gen = 0  # Génération courante i.e. ~âge de la population
        self._seq = seq  # Séquence à l'étude i.e. fichier fasta converti en chaine de caractère
        # Index de l'invidu au meilleur score à la génération courante
        self._current_best_distance_index = 0
        self._current_best_angle_index = 0
        for e in range(n):
            # On ajoute à la population un individu généré aléatoirement avec
            # un score à None par défaut
            self.add_to_pop(RotTable(randomGen=True), None)

        

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

    def _Get_Current_Best_Distance(self):
        return None if self._current_best_distance_index is None else self._pop[self._current_best_distance_index]

    def _Get_Current_Best_Distance_Index(self):
        return self._current_best_distance_index
    
    def _Get_Current_Best_Angle(self):
        return None if self._current_best_angle_index is None else self._pop[self._current_best_angle_index]

    def _Get_Current_Best_Angle_Index(self):
        return self._current_best_angle_index

    #################
    # MODIFICATEURS #
    #################

    def add_to_pop(self, individual, score=None):
        self._pop.append([individual, score])

    def del_from_pop(self, rang):
        if not isinstance(rang, int) and rang in range(len(self._pop)):
            raise Exception("Rang must be an int")
        del(self._pop[rang])

    def update_current_gen(self):
        self._current_gen += 1

    def set_pop(self, liste):
        if not isinstance(liste, list):
            raise Exception("Liste must be a list type")
        self._pop = liste[:]

    def clear_pop(self):
        self.set_pop([])

    def update_current_best_angle_index(self, new_best_index):
        self._current_best_angle_index = new_best_index

    def update_current_best_distance_index(self, new_best_index):
        self._current_best_distance_index = new_best_index

    ########################
    # FONCTIONS EVOLUTIVES #
    ########################

    def eval_pop_scaling(self, N):
        ''' Modifie la fonction d'évaluation avec du scaling pour moins converger localement, en particulier au début
        Nécessite N le nombre de génération total prévu '''
        if not isinstance(N, int):
            raise Exception("N must be an int")
        p = 0.1
        n = self._current_gen
        if n == 0:
            k = (np.tan((n + 1 / (N + 1)) * np.pi / 2))**p
        else:
            k = (np.tan((n / (N + 1)) * np.pi / 2))**p
        # k commence proche de 0 donc lisse les scores, puis augmente en passant par 1 ;
        # plus N est grand, plus k augmente, à terme ; pour N à 1000000, k vaut
        # environ 3 à la dernière génération
        current_best_distance_score = math.inf
        best_indiv_distance_index = 0
        current_best_angle_score = 0
        best_indiv_angle_index = 0
        for i in range(len(self._pop)):  # On parcourt la population...
            (distance, angle)= self._pop[i][0].Evaluation2(self._seq)
            distance = distance**k
            if distance < current_best_distance_score:
                best_indiv_distance_index = i
                current_best_distance_score = distance
            if angle > current_best_angle_score:
                best_indiv_angle_index = i
                current_best_angle_score = angle
            # ...et on affecte à chaque individu son nouveau score
            self._pop[i][1] = (distance, angle)
        self.update_current_best_distance_index(best_indiv_distance_index)
        self.update_current_best_angle_index(best_indiv_angle_index)
        if best_indiv_distance_index != best_indiv_angle_index:
            return self._pop.pop(best_indiv_angle_index)
        else:
            return None


    def eval_pop(self):
        ''' Attribue un score à chaque individu de la population '''
        current_best_distance_score = math.inf
        best_indiv_distance_index = 0
        current_best_angle_score = 0
        best_indiv_angle_index = 0
        for i in range(len(self._pop)):  # On parcourt la population...
            (distance, angle) = self._pop[i][0].Evaluation2(self._seq)
            if distance < current_best_distance_score:
                best_indiv_distance_index = i
                current_best_distance_score = distance
            if angle > current_best_angle_score:
                best_indiv_angle_index = i
                current_best_angle_score = angle
            # ...et on affecte à chaque individu son nouveau score
            self._pop[i][1] = (distance, angle)
        self.update_current_best_distance_index(best_indiv_distance_index)
        self.update_current_best_angle_index(best_indiv_angle_index)
        if best_indiv_distance_index != best_indiv_angle_index:
            return self._pop.pop(best_indiv_angle_index)
        else:
            return None

    def select_elite_pop(self, coefficient=0.5):
        '''Fonction de sélection par élitisme de la population : ne garde que les "coefficient%" individus de score le plus bas'''
        if (not isinstance(coefficient, float)) and (
                coefficient > 1 or coefficient < 0):
            raise Exception("coefficient must be a float between 0 and 1 ")
        # On récupère la liste de la population triée par scores
        L = sorted(self._pop, key=lambda x: x[1][0])
        n = len(self._pop)
        self.clear_pop()  # On efface l'ancienne population
        for i in range(1, int(n * coefficient)):  # Et on rajoute les n*coefficients premiers/meilleurs
            self._pop.append(L[i])
        self._pop.append(L[0])
        self.update_current_best_distance_index(len(self._pop) - 1)

    def select_tournoi_pop(self, luck_prob, puissance):
        '''Fonction de sélection par tournoi de la population ; il y a une probabilité que le plus faible des combattants
        (plus haut score) gagne quand même : proba ; celle-ci dépend de la différence de score entre les deux combattants
        et on peut ajouter un paramètre luck_prob qui pondère cette probabilité ; à noter que le meilleur individu est
        exempt de cette probabilité pour être certain qu'il n'est pas éliminé.

        Par défaut, luck_prob = 0 et puissance = 2, cf evolve. '''
        if not isinstance(
                luck_prob, float) and (
                luck_prob > 1 or luck_prob < 0):
            raise Exception(
                "Luck_prob should be a float value between 0 and 1")
        if not isinstance(puissance, int):
            raise Exception("Puissance should be an integer")
        best_individu = self._pop.pop(self._current_best_distance_index)
        L = []  # Tableau des vainqueurs
        n = len(self._pop)  # Taille de la population
        # Liste des indices des individus n'ayant pas encore combattu
        remaining = [i for i in range(n)]
        while n > 1:
            i1 = np.random.randint(0, n)  # On tire un 1er nombre au hasard...
            # ...qui nous donne l'indice d'un individu à faire combattre
            j1 = remaining.pop(i1)
            # On tire un 2e nombre au hasard...
            i2 = np.random.randint(0, n - 1)
            # ...qui nous donnent l'indice d'un autre individu à faire combattre
            j2 = remaining.pop(i2)
            score1 = self._pop[j1][1][0]
            score2 = self._pop[j2][1][0]
            diff = score1 - score2
            if diff < 0:
                proba = (1 - (-diff / score2)**puissance) * luck_prob
                if np.random.random() < proba:
                    L.append(self._pop[j2])
                else:
                    L.append(self._pop[j1])
            else:
                proba = (1 - (diff / score1)**puissance) * luck_prob
                if np.random.random() < proba:
                    L.append(self._pop[j1])
                else:
                    L.append(self._pop[j2])
            # L.append(self._pop[j1 if self._pop[j1][1]<self._pop[j2][1] else
            # j2]) # On ajoute alors à L l'individu vainqueur du combat
            n -= 2
        self.clear_pop()  # On vide l'ancienne population
        for individu in L:  # Et on rajoute tous les vainqueurs
            self._pop.append(individu)
        self._pop.append(best_individu)
        self.update_current_best_distance_index(len(self._pop) - 1)

    def mutate_pop(self, alpha, adapt_var, best_angle):
        ''' Mutation de tous les individus composant notre population avec une probabilité alpha (par défaut 0.01 tel que
        déterminé dans evolve) SAUF le meilleur individu qui n'est jamais muté si cette mutation est a posteriori
        dégradante. '''
        if not isinstance(alpha, float) and (alpha > 1 or alpha < 0):
            raise Exception("alpha should be a float value between 0 and 1")
        best_distance = self._pop.pop()
        mutate_best_distance = RotTable(rot_dict=copy.deepcopy(best_distance[0].getRotTable()))  # et on le duplique
        if best_angle is None:
            best_angle = [RotTable(rot_dict=copy.deepcopy(best_distance[0].getRotTable())),best_distance[1]]
        mutate_best_angle = RotTable(rot_dict=copy.deepcopy(best_angle[0].getRotTable()))
        # On fait muter la copie du meilleur (de manière certaine)
        mutate_best_distance.Mutate(self._current_gen, adapt_var)
        mutate_best_angle.Mutate(self._current_gen, adapt_var)
        mutate_best_distance_eval = mutate_best_distance.Evaluation2(
            self._seq)  # et on calcule son score
        mutate_best_angle_eval = mutate_best_angle.Evaluation2(
            self._seq)
            
        n = len(self._pop)
        # On génère le nombre d'individus à muter...
        k = np.random.binomial(n, alpha)
        individuals_to_mutate = np.random.randint(
            0, n, k)  # ...et on en génère autant d'indices

        for i in individuals_to_mutate:  # On parcourt les indices des individus à muter...
            # ...et on fait muter chaque individu correspondant
            self._pop[i][0].Mutate(self._current_gen, adapt_var)

        # Si la mutation du meilleur est encore meilleure...
        if mutate_best_distance_eval[0] < best_distance[1][0]:
            # ...on l'ajoute à la population
            self._pop.append([mutate_best_distance, mutate_best_distance_eval])
        else:
            self._pop.append(best_distance)  # Sinon on rajoute le meilleur
        if mutate_best_angle_eval[1] > best_angle[1][1]:
            # ...on l'ajoute à la population
            self._pop.append([mutate_best_angle, mutate_best_angle_eval])
        else:
            self._pop.append(best_angle)
        self.update_current_best_distance_index(len(self._pop) - 2)
        self.update_current_best_angle_index(len(self._pop) - 1)

    def cross_pop(self):
        '''Fonction de croisement de la population : double sa taille'''
            
        best_angle = self._pop.pop()
        n = len(self._pop)
        k = n//2
        individuals_to_cross = np.random.randint(0, n, k)
        for i in individuals_to_cross:
            cut = np.random.randint(0, RotTable._RotTable__NUM_KEYS)
            cross_1, cross_2 = self._pop[i][0].Cross(best_angle[0], cut)
            self.add_to_pop(cross_1)
            self.add_to_pop(cross_2)

        self._pop.append(best_angle)
        self.update_current_best_angle_index(len(self._pop)-1)


    ############################
    # ITERATION DE GENERATIONS #
    ############################

    def next_gen(
            self,
            n,
            scaling,
            selection_method,
            alpha,
            luck_prob,
            puissance,
            adapt_var):
        ''' Passage à la génération suivante : une itération de la boucle évaluation, sélection, croisement, mutation
        On peut choisir
        - la méthode de sélection choisie entre tournoi et élitisme avec selection_method = "Tournoi" par défaut
        - l'évaluation avec ou sans scaling avec le paramètre scaling = False par défaut
        - le paramètre alpha =  0.01 par défaut qui correspond au taux de mutation (chance qu'une mutation ait lieu par génération)
        On trouve également les luck_prob et puissance associés à la sélection par tournoi, et n le nombre de générations
        étudié, nécessaire pour calculer l'évaluation avec scaling. '''
        if not isinstance(n, int):
            raise Exception("n should be an integer")
        if not (scaling or scaling == False):
            raise Exception("scaling should be a boolean")
        # les types des autres variables sont tester dans l'entrée des autres
        # méthodes
        best_angle = None
        if scaling:
            best_angle = self.eval_pop_scaling(n)
        else:
            best_angle_ = self.eval_pop()
        if selection_method == "Elitisme":
            self.select_elite_pop()
        elif selection_method == "Tournoi":
            self.select_tournoi_pop(luck_prob, puissance)
        else:
            raise Exception(
                " selection_method must be either 'Elitisme' or 'Tournoi'")
        self.mutate_pop(alpha, adapt_var, best_angle)
        self.cross_pop()
        self.update_current_gen()
        #print("Taille de la population :",len(self._pop))

    def evolve(
            self,
            n,
            scaling=False,
            selection_method="Tournoi",
            alpha=0.59,
            luck_prob=0,
            puissance=2,
            adapt_var=True):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération. Ce sont ses paramètres qui déterminent ceux de toutes
        les autres fonctions évolutionnaires utilisées car c'est la fonction qu'on appelle dans main.'''

        for i in range(
                n - 1):  # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(
                n,
                scaling,
                selection_method,
                alpha,
                luck_prob,
                puissance,
                adapt_var)
        self.eval_pop()  # pour avoir une population dont tous les individus ont un score


    def evolve_with_step(
            self,
            n,
            step,
            scaling=False,
            alpha=0.59,
            selection_method="Tournoi",
            luck_prob=0,
            puissance=2,
            adapt_var=True):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération. Ce sont ses paramètres qui déterminent ceux de toutes
        les autres fonctions évolutionnaires utilisées car c'est la fonction qu'on appelle dans main.'''
        C = []
        for i in range(
                n - 1):  # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(
                n,
                scaling,
                selection_method,
                alpha,
                luck_prob,
                puissance,
                adapt_var)
            if i % step == 0:
                C.append(self._pop[self._current_best_distance_index][1][0])
        self.eval_pop()  # pour avoir une population dont tous les individus ont un score
        if (n - 1) % step == 0:
            C.append(self._pop[self._current_best_distance_index][1][0])
        return C

    def evolve_and_graph(
            self,
            n,
            scaling=False,
            alpha=0.59,
            selection_method="Tournoi",
            luck_prob=0,
            puissance=2,
            adapt_var=True):
        ''' Exécute l'algo génétique en s'arrêtant à la n-1e génération et trace le graphe de convergence  '''
        x = []
        y = []
        for i in range(
                n - 1):  # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(
                n,
                scaling,
                selection_method,
                alpha,
                luck_prob,
                puissance,
                adapt_var)
            new_y = self._pop[self._current_best_distance_index][1][0]
            y.append(new_y)
            x.append(self._current_gen)
            print("Le meilleur individu a un score de :", new_y, "\n")
        self.eval_pop()  # pour avoir une population dont tous les individus ont un score
        print("Dernière génération :", self._current_gen)
        print("Le meilleur individu a un score de :",
              self._pop[self._current_best_distance_index][1][0], "\n")
        y.append(self._pop[self._current_best_distance_index][1][0])
        x.append(self._current_gen + 1)
        fig, ax = plt.subplots()
        plt.xlabel('Nombre de générations')
        plt.ylabel('Meilleur score')
        plt.title(
            'Evolution du meilleur score de la population au fil des générations')
        plt.plot(x, y, 'ro--')
        plt.savefig("Output/Convergence{}_{}_{}_{}_{}.png".format(n,
                                                                  scaling, selection_method, luck_prob, puissance))
        plt.show()


    def evolve_double_graph(
            self,
            n,
            scaling=False,
            alpha=0.59,
            selection_method="Tournoi",
            luck_prob=0,
            puissance=2,
            adapt_var=True):
        host = host_subplot(111, axes_class=AA.Axes)
        #plt.subplots_adjust(right=0.9)
        par1 = host.twinx()
        new_fixed_axis = par1.get_grid_helper().new_fixed_axis
        par1.axis["right"] = new_fixed_axis(loc="right", axes=par1)

        par1.axis["right"].toggle(all=True)

        #host.set_xlim(1, n-1)
        #host.set_ylim(0, 1500)
        #par1.set_ylim(-1, 1)

        host.set_xlabel("Générations")
        host.set_ylabel("Meilleure distance")
        par1.set_ylabel("Meilleur angle")
        
        x = []
        distances = []
        angles = []
        for i in range(n - 1):  # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
            self.next_gen(
                n,
                scaling,
                selection_method,
                alpha,
                luck_prob,
                puissance,
                adapt_var)
            new_distance = self._pop[self._current_best_distance_index][1][0]
            new_angle = self._pop[self._current_best_angle_index][1][1]
            distances.append(new_distance)
            angles.append(new_angle)
            x.append(self._current_gen)

        p1, = host.plot(x, distances, 'ro--', label="Distance")
        p2, = par1.plot(x, angles, 'go--',  label="Angle")

        host.legend()

        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())

        plt.draw()
        plt.show()
        print("Meilleure distance: ", distances[-1], "Meilleur angle: ", angles[-1])
        plt.savefig("Output/Population_100_generations_300_double_score.png")
        self.dump_best_individu()

    def dump_best_individu(self):
        pickle.dump(self._pop[self._current_best_distance_index], open("Output/Best_distance_individu__5.p", "wb"))
        pickle.dump(self._pop[self._current_best_angle_index], open("Output/Best_angle_individu__5.p", "wb"))

