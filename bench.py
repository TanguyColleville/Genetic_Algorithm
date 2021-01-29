from Population import Population
# from scipy.optimize import minimize_scalar
import numpy as np
np.random.seed(1)
# from sklearn.linear_model import SGDRegressor
import matplotlib.pyplot as plt 
import pickle as p 


lineList = [line.rstrip('\n') for line in open("Data\plasmid_8k.fasta")]
seq = ''.join(lineList[1:])

def best_score(nbindiv,nbgen,methode="Tournoi",alpha=0.59):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha)
    return pop._Get_Current_Best()[1]

####Elite VS Tournoi 
X=[i for i in range(100,5100,100)]# indivdu 
Y=[j for j in range(25,325,25)]# nb de génération
x,y=np.meshgrid(X,Y)#,spare=True)
x_flat=x.flatten()
y_flat=y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
tournoi=np.array([[best_score(X[i],Y[j],"Tournoi") for i in range(len(X))] for j in range(len(Y))])
elitisme=np.array([[best_score(X[i],Y[j],"Elitisme") for i in range(len(X))] for j in range(len(Y))])
p.dump(tournoi, open("Output\Benchmark_Tournoi-Elitisme_tournoi.p", "wb"))
p.dump(elitisme, open("Output\Benchmark_Tournoi-Elitisme_elitisme.p", "wb"))
Z=np.array([[tournoi[j][i]-elitisme[j][i] for i in range(len(X))] for j in range(len(Y))])
ax.plot_wireframe(x, y, Z,color="red",label="Tournoi-Elitisme")
plt.legend()
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
plt.savefig("Output\Tournoi_vs_Elitisme.png")
plt.show()


# ### Tournoi VS Tournoi avec proba gain du faible
def best_score_luck(nbindiv,nbgen,methode="Tournoi",alpha=0.59,luck_prob=0):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha,luck_prob=luck_prob)
    return pop._Get_Current_Best()[1]

X=[i for i in range(200,2200,500)]# indivdu 
Y=[j for j in range(50,550,10)]# nb de génération
x,y=np.meshgrid(X,Y)#,spare=True)
x_flat=x.flatten() 
y_flat=y.flatten()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Not_Lucky=np.array([[best_score_luck(X[i],Y[j],"Elitisme",luck_prob=0) for i in range(len(X))] for j in range(len(Y))])
p.dump(Not_Lucky, open("Output\Benchmark_Not_Lucky.p", "wb"))
Quite_Lucky=np.array([[best_score_luck(X[i],Y[j],"Tournoi",luck_prob=0.25) for i in range(len(X))] for j in range(len(Y))])
p.dump(Quite_Lucky, open("Output\Benchmark_Quite_Lucky.p", "wb"))
Semi_Lucky=np.array([[best_score_luck(X[i],Y[j],"Tournoi",luck_prob=0.5) for i in range(len(X))] for j in range(len(Y))])
p.dump(Semi_Lucky, open("Output\Benchmark_Semi_Lucky.p", "wb"))
Pretty_Lucky=np.array([[best_score_luck(X[i],Y[j],"Tournoi",luck_prob=0.75) for i in range(len(X))] for j in range(len(Y))])
p.dump(Pretty_Lucky, open("Output\Benchmark_Pretty_Lucky.p", "wb"))
Very_Lucky=np.array([[best_score_luck(X[i],Y[j],"Tournoi",luck_prob=1) for i in range(len(X))] for j in range(len(Y))])
p.dump(Very_Lucky, open("Output\Benchmark_Very_Lucky.p", "wb"))

# Z=np.array([[Lucky[j][i]-Not_Lucky[j][i] for i in range(len(X))] for j in range(len(Y))])

ax.plot_wireframe(x, y, Not_Lucky,label="Not_Lucky")
ax.plot_wireframe(x, y, Quite_Lucky,label="Quite_Lucky")
ax.plot_wireframe(x, y, Semi_Lucky,label="Semi_Lucky")
ax.plot_wireframe(x, y, Pretty_Lucky,label="Pretty_Lucky")
ax.plot_wireframe(x, y, Very_Lucky,label="Very_Lucky")
plt.legend()
plt.title("Comparaison de l'impact de la chance dans le gain du faible")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
plt.savefig("Output/Proba_NonProba.png")
plt.show()

## Scaling

def best_score_Scaling(nbindiv,nbgen,methode="Tournoi",alpha=0.59,scaling=0):
    pop = Population(seq,nbindiv)
    pop.evolve(nbgen,methode, alpha=alpha,scaling=scaling)
    return pop._Get_Current_Best()[1]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
Scaled=np.array([[best_score_Scaling(int(X[i]),Y[j],"Tournoi",scaling=True) for i in range(len(X))] for j in range(len(Y))])
p.dump(Scaled, open("Output\Benchmark_Scaled.p", "wb"))

Non_Scaled=np.array([[best_score_Scaling(int(X[i]),Y[j],"Tournoi",scaling=False) for i in range(len(X))] for j in range(len(Y))])
p.dump(Non_Scaled, open("Output\Benchmark_Non_Scaled.p", "wb"))

Z=np.array([[Scaled[j][i]-Non_Scaled[j][i] for i in range(len(X))] for j in range(len(Y))])

ax.plot_wireframe(x, y, Z,color="red",label="Scaling True - False")
plt.legend()
plt.title("Surface Scaling - Non Scaling")
plt.xlabel("Nombre d'individus")
plt.ylabel("Nombre de générations")
plt.savefig("Output\Scaling_NonSCaling.png")
plt.show()

