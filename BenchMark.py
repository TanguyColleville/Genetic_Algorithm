from Population import Population
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D



lineList = [line.rstrip('\n') for line in open("Data\plasmid_8k.fasta")]
seq = ''.join(lineList[1:])


def best_score(nbindiv,nbgen,methode="Tournoi",alpha=0.59):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha)
    return pop._Get_Current_Best()[1]

####Elite VS Tournoi 
X=[i for i in range(100,500,100)]# indivdu 
Y=[j for j in range(10,50,10)]# nb de génération
i=0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coloration=["green","red"]
for meth in ["Tournoi","Elitisme"]:
    Z=np.array([best_score(X[i],Y[j],meth) for i in range(len(X)) for j in range(len(Y))])
    ax.plot_wireframe(X, Y, np.reshape(Z,(-1,2)),color=coloration[i],label="{}".format(meth))
    i+=1
plt.legend()
plt.show()

### Tournoi VS Tournoi avec proba gain du faible
def best_score_luck(nbindiv,nbgen,methode="Tournoi",alpha=0.59,luck_prob=0):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha,luck_prob=luck_prob)
    return pop._Get_Current_Best()[1]

i=0
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coloration=["green","red"]
for luck in range(2):
    Z=np.array([best_score_luck(X[i],Y[j],"Tournoi",luck_prob=luck) for i in range(len(X)) for j in range(len(Y))])
    ax.plot_wireframe(X, Y, np.reshape(Z,(-1,2)),color=coloration[i],label="Prob {}".format(luck))
    i+=1
plt.legend()
plt.show()
### Scaling VS Sans Scaling 
def best_score_Scaling(nbindiv,nbgen,methode="Tournoi",alpha=0.59,scaling=0):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha,scaling=scaling)
    return pop._Get_Current_Best()[1]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
coloration=["green","red"]
for scal in range(2):
    Z=np.array([best_score_Scaling(X[i],Y[j],"Tournoi",scaling=scal) for i in range(len(X)) for j in range(len(Y))])
    ax.plot_wireframe(X, Y, np.reshape(Z,(-1,2)),color=coloration[i],label="Scaling {}".format(scal))
    i+=1
plt.legend()
plt.show()

