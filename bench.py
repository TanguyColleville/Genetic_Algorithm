import matplotlib.pyplot as plt
import numpy as np
import pickle as p


from Population import Population

np.random.seed(1)

lineList = [line.rstrip('\n') for line in open(r"Data/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])


def best_score(nbindiv, nbgen, step, methode="Tournoi", alpha=0.59):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode donnée
    à partir d'un nombre d'individu et d'un nombre de génération """
    pop = Population(seq, nbindiv)
    return pop.evolve_with_step(nbgen, step , selection_method=methode, alpha=alpha)


# Elite VS Tournoi
X = [i for i in range(100, 700, 100)]  # plage d'individus
Y = [j for j in range(0, 151, 2)]  # plage de génération
x, y = np.meshgrid(X, Y)
x_flat = x.flatten()
y_flat = y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
tournoi = np.array([best_score(X[i], 151, 2, "Tournoi") for i in range(len(X))])
# on enregistre les calculs pour tournoi
p.dump(tournoi, open(r"Output/Benchmark_Tournoi-Elitisme_tournoi.p", "wb"))

elitisme = np.array([best_score(X[i], 151, 2, "Elitisme") for i in range(len(X))])
# on enregistre les calculs pour Elitisme
p.dump(elitisme, open(r"Output/Benchmark_Tournoi-Elitisme_elitisme.p", "wb"))

Z = np.array([[tournoi[i][j] - elitisme[i][j] for i in range(len(X))] for j in range(len(Y))])
# on affiche la différence entre les deux afin d'etudier la performance
# des modèles de sélection
ax.plot_wireframe(x, y, Z, color="red", label="Tournoi-Elitisme")
plt.legend()
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.title("Comparaison de méthode de sélection : Elitisme vs Tournoi ")
plt.savefig(r"Output/Tournoi_vs_Elitisme.png")
plt.show()

# # étude de la performance de l'affectation d'une probabilité au gain d'un individu faible
# # Tournoi VS Tournoi avec proba gain d'in individu faible face à un
# # individu fort


# def best_score_luck(
#         nbindiv,
#         nbgen,
#         methode="Tournoi",
#         alpha=0.59,
#         luck_prob=0):
#     """ Permet de calculer le score du meilleur individu de la population pour la méthode Tournoi à partir d'un nombre d'individu
#      , d'un nombre de génération et d'une probabilité de gain du faible face à un individu fort"""
#     pop = Population(seq, nbindiv)
#     pop.evolve(nbgen, selection_method=methode, alpha=alpha, luck_prob=luck_prob)
#     return pop._Get_Current_Best()[1]


# X = [i for i in range(200, 2200, 500)]  # plage d'indivdu
# Y = [j for j in range(50, 550, 10)]  # plage de génération
# x, y = np.meshgrid(X, Y)
# x_flat = x.flatten()
# y_flat = y.flatten()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # On enregiste les calculs pour différentes valeurs de probabilité

# Not_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0)
#                        for i in range(len(X))] for j in range(len(Y))])
# p.dump(Not_Lucky, open(r"Output/Benchmark_Not_Lucky.p", "wb"))
# Quite_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.25)
#                          for i in range(len(X))] for j in range(len(Y))])
# p.dump(Quite_Lucky, open(r"Output/Benchmark_Quite_Lucky.p", "wb"))
# Semi_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.5)
#                         for i in range(len(X))] for j in range(len(Y))])
# p.dump(Semi_Lucky, open(r"Output/Benchmark_Semi_Lucky.p", "wb"))
# Pretty_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.75)
#                           for i in range(len(X))] for j in range(len(Y))])
# p.dump(Pretty_Lucky, open(r"Output/Benchmark_Pretty_Lucky.p", "wb"))
# Very_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=1)
#                         for i in range(len(X))] for j in range(len(Y))])
# p.dump(Very_Lucky, open(r"Output/Benchmark_Very_Lucky.p", "wb"))

# # On affiche les résultats en wireframe

# ax.plot_wireframe(x, y, Not_Lucky, label="Not_Lucky")
# ax.plot_wireframe(x, y, Quite_Lucky, label="Quite_Lucky")
# ax.plot_wireframe(x, y, Semi_Lucky, label="Semi_Lucky")
# ax.plot_wireframe(x, y, Pretty_Lucky, label="Pretty_Lucky")
# ax.plot_wireframe(x, y, Very_Lucky, label="Very_Lucky")
# plt.legend()
# plt.title("Comparaison de l'impact de la probabilité de gain du faible")
# plt.xlabel("Nombre d'individus")
# plt.ylabel("Nombre de générations")
# ax.set_zlabel('Score')
# plt.savefig("Output/Proba_NonProba.png")
# plt.show()


# # étude de la performance du scaling

'''
def best_score_Scaling(
        nbindiv,
        nbgen,
        step,
        methode="Tournoi",
        alpha=0.59,
        scaling=0):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode à partir d'un nombre d'individu
     , d'un nombre de génération avec ou sans Scaling """
    pop = Population(seq, nbindiv)
    y = pop.evolve_with_step(nbgen, step,scaling=scaling, alpha=alpha, selection_method = methode)
    return y


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#X = [100, 250, 500, 750, 1000]
X = [100, 300]
print(X)
nbgen = 501
step = 5
Y = [j for j in range(0,nbgen,step)]
print(Y)
Scaled = np.array([best_score_Scaling(int(X[i]), nbgen, step, "Tournoi", scaling=True) for i in range(len(X))])
# on enregistre le calcul avec scaling
p.dump(Scaled, open(r"Output\Benchmark_Scaled.p", "wb"))

Non_Scaled = np.array([best_score_Scaling(int(X[i]), nbgen, step, "Tournoi", scaling=False) for i in range(len(X))])

# on enregistre le calcul sans scaling
p.dump(Non_Scaled, open(r"Output\Benchmark_Non_Scaled.p", "wb"))

#Z = np.array([[Scaled[j][i] - Non_Scaled[j][i] for i in range(len(X))] for j in range(len(Y))])  # on calcule la différence
Z = Scaled - Non_Scaled
#Z = np.zeros((len(X), len(Y)))
#for i in range(len(X)):
#    for j in range(len(Y)):
#        Z[i][j] = i + j

x, y = np.meshgrid(X, Y, sparse = True, indexing = 'ij')

ax.plot_wireframe(x, y, Z, color="red", label="Scaling True - False")
plt.legend()
plt.title("Surface Scaling - Non Scaling")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.savefig(r"Output\Scaling_NonSCaling.png")
plt.show()
'''


# ## Etude de l'influence de la probabilité de mutation d'un individu à chaque génération

'''
def best_score_alpha(
        nbindiv,
        nbgen,
        methode="Tournoi",
        alpha=0.59,
        scaling=0,
        luck_prob = 0,
        puissance = 2):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode à partir d'un nombre d'individu,
    d'un nombre de génération en faisant varier alpha"""
    pop = Population(seq, nbindiv)
    y = []
    for i in range(nbgen - 1):  # on s'arrête à la génération n-1 pour ne pas renvoyer une pop mutée
        pop.next_gen(
            nbgen,
            scaling,
            methode,
            alpha,
            luck_prob,
            puissance)
        new_y = pop._pop[pop._current_best_index][1]
        y.append(new_y)
    pop.eval_pop()  # pour avoir une population dont tous les individus ont un score
    y.append(pop._pop[pop._current_best_index][1])
    return y

alphas = [0.01, 0.25, 0.5, 0.75, 0.9]    
y1 = best_score_alpha(100, 200, methode = "Tournoi", alpha = alphas[0], scaling = False)
p.dump(y1, open(r"Output\alpha_0.01", "wb"))
y2 = best_score_alpha(100, 200, methode = "Tournoi", alpha = alphas[1], scaling = False)
p.dump(y2, open(r"Output\alpha_0.25", "wb"))
y3 = best_score_alpha(100, 200, methode = "Tournoi", alpha = alphas[2], scaling = False)
p.dump(y3, open(r"Output\alpha_0.5", "wb"))
y4 = best_score_alpha(100, 200, methode = "Tournoi", alpha = alphas[3], scaling = False)
p.dump(y4, open(r"Output\alpha_0.75", "wb"))
y5 = best_score_alpha(100, 200, methode = "Tournoi", alpha = alphas[4], scaling = False)
p.dump(y5, open(r"Output\alpha_0.9", "wb"))
coloration = ["r-", "g-", "b-", "k-", "c-"]
x = [i for i in range(200)]  
fig, ax = plt.subplots()
plt.xlabel('Nombre de générations')
plt.ylabel('Meilleur score')
plt.title('Evolution du meilleur score de la population au fil des générations')
plt.plot(x, y1, coloration[0], label = '0.01')  
plt.plot(x, y2, coloration[1], label = '0.25') 
plt.plot(x, y3, coloration[2], label = '0.5') 
plt.plot(x, y4, coloration[3], label = '0.75') 
plt.plot(x, y5, coloration[4], label = '0.9')  
plt.legend()
plt.savefig(r"Output\differents_alpha_pop_100_gen_200_non_scaled.png")
plt.show()
'''

# # étude de la performance du scaling


# def best_score_Adapt_var(
#         nbindiv,
#         nbgen,
#         adapt_var):
#     """ Permet de calculer le score du meilleur individu de la population pour une méthode à partir d'un nombre d'individu
#      , d'un nombre de génération avec ou sans Scaling """
#     pop = Population(seq, nbindiv)
#     pop.evolve(nbgen, adapt_var=adapt_var)
#     return pop._Get_Current_Best()[1]


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# Adapt_var = np.array([[best_score_Adapt_var(int(X[i]), Y[j], True)
#                     for i in range(len(X))] for j in range(len(Y))])
# # on enregistre le calcul avec adapt_var
# p.dump(Adapt_var, open(r"Output/Benchmark_Adapt_var.p", "wb"))

# Not_Adapt_var = np.array([[best_score_Adapt_var(int(X[i]), Y[j], False)
#                         for i in range(len(X))] for j in range(len(Y))])
# # on enregistre le calcul sans adapt_var
# p.dump(Not_Adapt_var, open(r"Output/Benchmark_Not_Adapt_var.p", "wb"))

# Z = np.array([[Adapt_var[j][i] - Not_Adapt_var[j][i] for i in range(len(X))]
#               for j in range(len(Y))])  # on calcule la différence

# ax.plot_wireframe(x, y, Z, color="red", label="Adapt_var True - False")
# plt.legend()
# plt.title("Surface Adapt_var - Not_Adapt_var")
# plt.xlabel("Nombre d'individus")
# plt.ylabel("Nombre de générations")
# ax.set_zlabel('Score')
# plt.savefig(r"Output/Adapt_var-Not_Adapt_var.png")
# plt.show()
