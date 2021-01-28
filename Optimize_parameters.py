from Population import Population
from scipy.optimize import minimize_scalar
import numpy as np
np.random.seed(1)


lineList = [line.rstrip('\n') for line in open("plasmid_8k.fasta")]
seq = ''.join(lineList[1:])
pop_size = 1000
nb_gen = 20

def best_score_given_mutation_probability(alpha):
    pop = Population(seq,pop_size)
    pop.evolve(nb_gen,"Tournoi", alpha=alpha)
    return pop._Get_Current_Best()[1]


# res = minimize_scalar(best_score_given_mutation_probability, bounds=(0, 1), method='bounded')

if res.success:
    print("Minimum trouvé !\n")
    print("Valeur minimale obtenue de",res.fun,"pour alpha =",res.x)
else:
    print("Pas de minimum trouvé...")


def best_score(list,alpha=0.59):

    pop = Population(seq,list[0])
    pop.evolve(list[1],"Tournoi", alpha=alpha)
    return pop._Get_Current_Best()[1]


X=[i for i in range(100,500,100)]
Y=[j for j in range(10,30,10)]
Z=[best_score(X[i]) for i in range(len(X))]

plt.figure()
Axes3D.plot_wireframe(X, Y, Z)
plt.show()

