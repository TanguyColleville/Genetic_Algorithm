import matplotlib.pyplot as plt
import numpy as np
import pickle as p


from Population import Population

np.random.seed(1)

lineList = [line.rstrip('\n') for line in open(r"Data/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])


def best_score(nbindiv, nbgen, methode="Tournoi", alpha=0.59):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode donnée
    à partir d'un nombre d'individu et d'un nombre de génération """
    pop = Population(seq, nbindiv)
    pop.evolve(nbgen, selection_method=methode, alpha=alpha)
    return pop._Get_Current_Best()[1]


# Elite VS Tournoi
X = [i for i in range(100, 5100, 100)]  # plage d'individus
Y = [j for j in range(25, 325, 25)]  # plage de génération
x, y = np.meshgrid(X, Y)
x_flat = x.flatten()
y_flat = y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
tournoi = np.array([[best_score(X[i], Y[j], "Tournoi")
                     for i in range(len(X))] for j in range(len(Y))])
# on enregistre les calculs pour tournoi
p.dump(tournoi, open(r"Output/Benchmark_Tournoi-Elitisme_tournoi.p", "wb"))

elitisme = np.array([[best_score(X[i], Y[j], "Elitisme")
                      for i in range(len(X))] for j in range(len(Y))])
# on enregistre les calculs pour Elitisme
p.dump(elitisme, open(r"Output/Benchmark_Tournoi-Elitisme_elitisme.p", "wb"))

Z = np.array([[tournoi[j][i] - elitisme[j][i]
               for i in range(len(X))] for j in range(len(Y))])
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

# étude de la performance de l'affectation d'une probabilité au gain d'un individu faible
# Tournoi VS Tournoi avec proba gain d'in individu faible face à un
# individu fort


def best_score_luck(
        nbindiv,
        nbgen,
        methode="Tournoi",
        alpha=0.59,
        luck_prob=0):
    """ Permet de calculer le score du meilleur individu de la population pour la méthode Tournoi à partir d'un nombre d'individu
     , d'un nombre de génération et d'une probabilité de gain du faible face à un individu fort"""
    pop = Population(seq, nbindiv)
    pop.evolve(nbgen, selection_method=methode, alpha=alpha, luck_prob=luck_prob)
    return pop._Get_Current_Best()[1]


X = [i for i in range(200, 2200, 500)]  # plage d'indivdu
Y = [j for j in range(50, 550, 10)]  # plage de génération
x, y = np.meshgrid(X, Y)
x_flat = x.flatten()
y_flat = y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# On enregiste les calculs pour différentes valeurs de probabilité

Not_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0)
                       for i in range(len(X))] for j in range(len(Y))])
p.dump(Not_Lucky, open(r"Output/Benchmark_Not_Lucky.p", "wb"))
Quite_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.25)
                         for i in range(len(X))] for j in range(len(Y))])
p.dump(Quite_Lucky, open(r"Output/Benchmark_Quite_Lucky.p", "wb"))
Semi_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.5)
                        for i in range(len(X))] for j in range(len(Y))])
p.dump(Semi_Lucky, open(r"Output/Benchmark_Semi_Lucky.p", "wb"))
Pretty_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=0.75)
                          for i in range(len(X))] for j in range(len(Y))])
p.dump(Pretty_Lucky, open(r"Output/Benchmark_Pretty_Lucky.p", "wb"))
Very_Lucky = np.array([[best_score_luck(X[i], Y[j], "Tournoi", luck_prob=1)
                        for i in range(len(X))] for j in range(len(Y))])
p.dump(Very_Lucky, open(r"Output/Benchmark_Very_Lucky.p", "wb"))

# On affiche les résultats en wireframe

ax.plot_wireframe(x, y, Not_Lucky, label="Not_Lucky")
ax.plot_wireframe(x, y, Quite_Lucky, label="Quite_Lucky")
ax.plot_wireframe(x, y, Semi_Lucky, label="Semi_Lucky")
ax.plot_wireframe(x, y, Pretty_Lucky, label="Pretty_Lucky")
ax.plot_wireframe(x, y, Very_Lucky, label="Very_Lucky")
plt.legend()
plt.title("Comparaison de l'impact de la probabilité de gain du faible")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.savefig("Output/Proba_NonProba.png")
plt.show()


# étude de la performance du scaling


def best_score_Scaling(
        nbindiv,
        nbgen,
        methode="Tournoi",
        alpha=0.59,
        scaling=0):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode à partir d'un nombre d'individu
     , d'un nombre de génération avec ou sans Scaling """
    pop = Population(seq, nbindiv)
    pop.evolve(nbgen, selection_method=methode, alpha=alpha, scaling=scaling)
    return pop._Get_Current_Best()[1]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Scaled = np.array([[best_score_Scaling(int(X[i]), Y[j], "Tournoi", scaling=True)
                    for i in range(len(X))] for j in range(len(Y))])
# on enregistre le calcul avec scaling
p.dump(Scaled, open(r"Output/Benchmark_Scaled.p", "wb"))

Non_Scaled = np.array([[best_score_Scaling(int(X[i]), Y[j], "Tournoi", scaling=False)
                        for i in range(len(X))] for j in range(len(Y))])
# on enregistre le calcul sans scaling
p.dump(Non_Scaled, open(r"Output/Benchmark_Non_Scaled.p", "wb"))

Z = np.array([[Scaled[j][i] - Non_Scaled[j][i] for i in range(len(X))]
              for j in range(len(Y))])  # on calcule la différence

ax.plot_wireframe(x, y, Z, color="red", label="Scaling True - False")
plt.legend()
plt.title("Surface Scaling - Non Scaling")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.savefig(r"Output/Scaling_NonSCaling.png")
plt.show()


## Etude de l'influence de la probabilité de mutation d'un individu à chaque génération


def best_score_alpha(
        nbindiv,
        nbgen,
        methode="Tournoi",
        alpha=0.59,
        luck_prob=0):
    """ Permet de calculer le score du meilleur individu de la population pour la méthode Tournoi à partir d'un nombre d'individu
     , d'un nombre de génération et d'une probabilité de mutation"""
    pop = Population(seq, nbindiv)
    pop.evolve(nbgen, selection_method=methode, alpha=alpha, luck_prob=luck_prob)
    return pop._Get_Current_Best()[1]


X = [i for i in range(200, 2200, 500)]  # plage d'indivdu
Y = [j for j in range(50, 550, 10)]  # plage de génération
x, y = np.meshgrid(X, Y)
x_flat = x.flatten()
y_flat = y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# On enregiste les calculs pour différentes valeurs de probabilité

No_Mutation = np.array([[best_score_alpha(X[i], Y[j], "Tournoi", alpha=0)
                       for i in range(len(X))] for j in range(len(Y))])
p.dump(No_Mutation, open(r"Output/Benchmark_No_Mutation.p", "wb"))
Few_Mutations = np.array([[best_score_alpha(X[i], Y[j], "Tournoi", alpha=0.25)
                         for i in range(len(X))] for j in range(len(Y))])
p.dump(Few_Mutations, open(r"Output/Benchmark_Few_Mutations.p", "wb"))
Some_Mutations = np.array([[best_score_alpha(X[i], Y[j], "Tournoi", alpha=0.5)
                        for i in range(len(X))] for j in range(len(Y))])
p.dump(Some_Mutations, open(r"Output/Benchmark_Some_Mutations.p", "wb"))
Lots_Mutations = np.array([[best_score_alpha(X[i], Y[j], "Tournoi", alpha=0.75)
                          for i in range(len(X))] for j in range(len(Y))])
p.dump(Lots_Mutations, open(r"Output/Benchmark_Lots_Mutations.p", "wb"))
Full_Mutations = np.array([[best_score_alpha(X[i], Y[j], "Tournoi", alpha=1)
                        for i in range(len(X))] for j in range(len(Y))])
p.dump(Full_Mutations, open(r"Output/Benchmark_Full_Mutations.p", "wb"))

# On affiche les résultats en wireframe

ax.plot_wireframe(x, y, No_Mutation, label="No_Mutation")
ax.plot_wireframe(x, y, Few_Mutations, label="Few_Mutations")
ax.plot_wireframe(x, y, Some_Mutations, label="Some_Mutations")
ax.plot_wireframe(x, y, Lots_Mutations, label="Lots_Mutations")
ax.plot_wireframe(x, y, Full_Mutations, label="Full_Mutations")
plt.legend()
plt.title("Comparaison de l'impact de la probabilité de mutation")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.savefig("Output/Proba_Mutation.png")
plt.show()


# étude de la performance du scaling


def best_score_Adapt_var(
        nbindiv,
        nbgen,
        adapt_var):
    """ Permet de calculer le score du meilleur individu de la population pour une méthode à partir d'un nombre d'individu
     , d'un nombre de génération avec ou sans Scaling """
    pop = Population(seq, nbindiv)
    pop.evolve(nbgen, adapt_var=adapt_var)
    return pop._Get_Current_Best()[1]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Adapt_var = np.array([[best_score_Adapt_var(int(X[i]), Y[j], True)
                    for i in range(len(X))] for j in range(len(Y))])
# on enregistre le calcul avec adapt_var
p.dump(Adapt_var, open(r"Output/Benchmark_Adapt_var.p", "wb"))

Not_Adapt_var = np.array([[best_score_Adapt_var(int(X[i]), Y[j], False)
                        for i in range(len(X))] for j in range(len(Y))])
# on enregistre le calcul sans adapt_var
p.dump(Not_Adapt_var, open(r"Output/Benchmark_Not_Adapt_var.p", "wb"))

Z = np.array([[Adapt_var[j][i] - Not_Adapt_var[j][i] for i in range(len(X))]
              for j in range(len(Y))])  # on calcule la différence

ax.plot_wireframe(x, y, Z, color="red", label="Adapt_var True - False")
plt.legend()
plt.title("Surface Adapt_var - Not_Adapt_var")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
ax.set_zlabel('Score')
plt.savefig(r"Output/Adapt_var-Not_Adapt_var.png")
plt.show()
