from RotTable import RotTable

table = {
        "AA": [9, 7.2, -154, 0.06, 0.6, 0],
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
    
seq="AAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCCAGTAAACGAAAAAACCGCCTGGGGAGGCGGTTTAGTCGAAGGTTAAGTCAG"

def test_init():
    rot = RotTable(rot_dict=table)
    assert rot.getTwist("AA") == 9

def test_str():
    rot = RotTable(randomGen=True)
    assert type(str(rot)) is str

def test_getTwist():
    rot = RotTable()
    assert rot.getTwist("AA") == 35.62

def test_getWedge():
    rot = RotTable()
    assert rot.getWedge("AA") == 7.2

def test_getDirection():
    rot = RotTable()
    assert rot.getDirection("AA") == -154

def test_getRotTable():
    rot=RotTable()
    assert type(rot.getRotTable()) is dict
    assert len(rot.getRotTable())==16

def test_Encodage():
    pass
def test_Mutate():
    rot=RotTable()
    

def test_evaluation():
    rot=RotTable()
    assert type(rot.Evaluation(seq)) is float

def test_Cross():
    pass

def test_correspondance():
    rot = RotTable()
    assert (rot.Correspondance('T') == 'A')  

def test_symetrique():
    rot = RotTable()
    assert (rot.Symetrique('AT') == 'AT')
    assert (rot.Symetrique('AG') == 'CT')

def test_reconstitution():
    rot = RotTable()
    l = len(rot.getRotTable())
    rot.Reconstitution()
    assert l != len(rot.getRotTable())
