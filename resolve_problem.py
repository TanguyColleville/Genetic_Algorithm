from Population import Population
import pickle
import numpy as np
np.random.seed(2)

lineList = [line.rstrip('\n') for line in open("./Data/plasmid_8k.fasta")]
seq = ''.join(lineList[1:])

pop = Population(seq,n=5)
pickle.dump(pop, open("Output/pop_ini.p", "wb"))
pop.eval_pop()
print(pop._Get_pop(),'\n')
pop.select_tournoi_pop(0.5,2)
print(pop._Get_pop())
#pop.eval_pop()
print(pop._Get_pop(),'\n')
pop.mutate_pop(0.59)
print(pop._Get_pop())
#pop.eval_pop()
print(pop._Get_pop(),'\n')
pop.cross_pop()
print(pop._Get_pop())
pop.eval_pop()
print(pop._Get_pop(),'\n\n\n')

pop2 = pickle.load(open("Output/pop_ini.p", "rb"))
pop2.eval_pop()
pop2.select_tournoi_pop(0.5,2)
pop2.mutate_pop(0.59)
pop2.cross_pop()
print(pop2._Get_pop(),'\n')
pop2.eval_pop()
print(pop2._Get_pop(),'\n\n\n')

