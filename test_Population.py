from Population import Population
import pytest

table = {
        "AA": [35.62, 7.2, -154, 0.06, 0.6, 0],
        "AC": [34.4, 1.1, 143, 1.3, 5, 0],
        "AG": [27.7, 8.4, 2, 1.5, 3, 0],
        "AT": [31.5, 2.6, 0, 1.1, 2, 0],
        "CA": [34.5, 3.5, -64, 0.9, 34, 0],
        "CC": [33.67, 2.1, -57, 0.07, 2.1, 0],
        "CG": [29.8, 6.7, 0, 1.1, 1.5, 0],
        "CT": [27.7, 8.4, -2, 1.5, 3, 0],
        "GA": [36.9, 5.3, 120, 0.9, 6, 0],
        "GC": [40, 5, 180, 1.2, 1.275, 0],
        "GG": [33.67, 2.1, 57, 0.07, 2.1, 0],
        "GT": [34.4, 1.1, -143, 1.3, 5, 0],
        "TA": [36, 0.9, 0, 1.1, 2, 0],
        "TC": [36.9, 5.3, -120, 0.9, 6, 0],
        "TG": [34.5, 3.5, 64, 0.9, 34, 0],
        "TT": [35.62, 7.2, 154, 0.06, 0.6, 0]
    }
    
seq = "AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG"

###################
# TEST ASSESSEURS #
################### 

def test_init():
    with pytest.raises(Exception(" seq must be a string which represents dinucleotides")):
        pop = Population(5)
    with pytest.raises(Exception(" n must be an integer greater than 1")):
        pop = Population(seq, n=0)

def test_assesseurs():
    pop = Population(seq, n=10)
    assert pop._Get_seq() == seq
    assert pop._Get_len() == 10
    assert pop._Get_Current_Gen() == 0
    assert pop._Get_Current_Best() is None

######################
# TEST MODIFICATEURS #
###################### 

def test_add_to_pop():
    pop = Population(seq)
    pop.add_to_pop(table)
    assert pop._Get_pop()[-1] == [table, None]
    pop.add_to_pop(table, 1)
    assert pop._Get_pop()[-1] == [table, 1]
 
def test_del_from_pop():
    pop = Population(seq)
    pop.add_to_pop(table, 1)
    pop.add_to_pop(table, 2)
    pop.del_from_pop(-1)
    assert pop._Get_pop()[-1] == [table, 1]

def test_update_current_gen():
    pop = Population(seq)
    ini = pop._Get_Current_Gen()
    pop.update_current_gen()
    assert pop._Get_Current_Gen() == ini + 1
    
def test_set_pop():
    pop = Population(seq)
    pop.set_pop([1,2,3])
    assert pop._Get_pop() == [1,2,3]

def test_clear_pop():
    pop = Population(seq)
    pop.clear_pop()
    assert pop._Get_pop() == []

def test_update_current_best():
    pop = Population(seq)
    pop.update_current_best(42)
    assert pop._Get_Current_Best() == 42 

def test_sort_pop_and_update_best():
    pop = Population(seq)
    pop.eval_pop()
    pop.sort_pop_and_update_best()
    assert pop._Get_pop() == sorted(pop._Get_pop(), key=itemgetter(1))
    assert pop._Get_Current_Best() is not None

    #############################
    # TEST FONCTIONS EVOLUTIVES #
    ############################# 

def test_eval_pop_scaling():
    pop = Population(seq)
    N = 5
    score = pop.eval_pop()
    pop.eval_pop_scaling(N)
    # pour n + 1 = 1 et N = 5, on a normalement k entre 0.876 et 0.877 (problème de stockage float, pas de test == )
    assert type(pop._Get_pop()[0][1]) is float
    assert pop._Get_pop()[0][1] < score**0.877 and score**0.876 < pop._Get_pop()[0][1] 


def test_eval_pop():
    pop = Population(seq)
    pop.eval_pop()
    assert type(pop._Get_pop()[0][1]) is float

def test_select_elite_pop():
    pop=Population(seq,n=10)
    Ini_len=len(pop._Get_pop())
    pop.eval_pop()
    pop.select_elite_pop(0.5)
    Post_len=len(pop._Get_pop())
    assert int(Ini_len*0.5)==int(Post_len)

def test_select_tournoi_pop():
    pop=Population(seq,n=10)
    Ini_len=len(pop._Get_pop())
    pop.eval_pop()
    pop.select_tournoi_pop()
    Post_len=len(pop._Get_pop())
    assert int(Ini_len*0.5)==int(Post_len)
    
def test_cross_pop():
    pop=Population(seq,n=10)
    Ini_len=len(pop._Get_pop())
    pop.cross_pop()
    Post_len=len(pop._Get_pop())
    assert int(Ini_len*2)==int(Post_len)

def test_mutate_pop(): 
    pop=Population(seq,n=5)
    pop.eval_pop()
    pop.sort_pop_and_update_best()
    initial_best_score = pop._Get_Current_Best()[1]
    pop.mutate_pop(0.59)
    best_score_after_mutation = pop._Get_Current_Best()[1]
    assert best_score_after_mutation >= initial_best_score
    
    
def test_next_gen():
    pop = Population(seq)
    initialGen = pop._Get_Current_Gen()
    pop.next_gen()
    assert pop._Get_Current_Gen() == initialGen + 1

def test_evolve():
    pop = Population(seq)
    initialGen = pop._Get_Current_Gen()
    pop.evolve(3)
    assert pop._Get_Current_Gen() == initialGen + 2
    pop = Population(seq)
    initialGen = pop._Get_Current_Gen()
    pop.evolve(3)

    
        
        