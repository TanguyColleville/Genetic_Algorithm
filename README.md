# Jeu évolutionnaire EI ST2 théorie des jeux 

On peut trouver le gitlab de notre groupe [ici](https://gitlab-cw2.centralesupelec.fr/tanguy.colleville/jeu_evolutionnaire)

Ce qu'on a accompli :

- [x] MVP : sélection élitiste, croisement en un point, pas de mutation
- [x] Mutations bruit gaussien
- [x] Rester dans les bornes (mutation et génération aléatoire)

A faire cet aprem : 

- [ ] Selection --> tournoi ou elitisme 
- [ ] Test et couverture des nouvelles méthodes 
- [ ] Symétrie 


## Membres : 
* Antony Perzo 
* Sébastien Liou 
* Timothée Grandchamp
* Tanguy Colleville 


## Liens utiles 
## Instruction pour installation 
On commence, pour travailler sur le projet ou le tester, par créer une copie locale avec `git clone https://gitlab-cw2.centralesupelec.fr/tanguy.colleville/jeu_evolutionnaire.git`
Ensuite, afin d'importer les modules nécessaires pour faire fonctionner correctement les programmes, il faut, dans une console Python, taper la requête " pip install -r requirements.txt " et simplement appuyer sur "entrée".
Nota Bene : il est préférable de travailler dans un environnement virtuel. Pour ce faire, il vous faut suivre ces étapes : 

se placer dans le rep du projet dans votre invite de commande
cd Python/repDuProjet (si on est à la racine)
Créer votre environnement virtuel via 
Python -m venv [NOM VENV]
Activer l’environnement : 
    si MACOS :
        source [NOM VENV]/bin/activate
    Si Windows :
        cd [NOM VENV] puis Scripts\Activate.bat
En demeurant dans [NOM VENV] taper pip install -r requirements.txt

## Structure 


## Utilisation


## Références 
[Real coded genetic algorithms (slides)](https://engineering.purdue.edu/~sudhoff/ee630/Lecture04.pdf)

