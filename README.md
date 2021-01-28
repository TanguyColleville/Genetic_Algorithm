# Jeu évolutionnaire EI ST2 théorie des jeux 

![CentraleSupelec Logo](https://www.centralesupelec.fr/sites/all/themes/cs_theme/medias/common/images/intro/logo_nouveau.jpg)
<div align=”center”>
![Projet Logo](logo_ei.png)
</div>

On peut trouver le gitlab de notre groupe [ici](https://gitlab-cw2.centralesupelec.fr/tanguy.colleville/jeu_evolutionnaire)

Ce qu'on a accompli :

- [x] MVP : sélection élitiste, croisement en un point, pas de mutation
- [x] Mutations bruit gaussien
- [x] Rester dans les bornes (mutation et génération aléatoire)
- [x] Symétrie 
- [x] Selection --> tournoi ou elitisme 
- [x] Interface utilisateur stylée
- [x] Ajouter bouton interface taille population
- [x] Ajouter bouton trajectoire 3D FINALE (ou le mettre dès qu'on calcule) 

A faire : 

- [ ] Test et couverture des nouvelles méthodes 
- [ ] Tester le meilleur entre tournoi et élitisme avec plusieurs seeds
- [ ] Optimiser pour ne jamais muter le meilleur ; modifier tournoi (% chance gagner même si moins bon score SAUF face au meilleur) ? pour plus de diversité ; croisement en deux points ?
- [ ] (Autres sélections ? roulette, rang)
- [ ] mutation auto-adaptative ? facile à implémenter +-
- [ ] changer évalutation prendre orientation des extrémités en compte (produit scalaire)


## Membres : 
* Antony Perzo 
* Sébastien Liou 
* Timothée Grandchamp
* Tanguy Colleville 


## Liens utiles 
* Miro [ici](https://miro.com/app/board/o9J_lXQ3JWY=/), il permet de mettre exergue la partie organisationnelle de notre projet ainsi que de comprendre la structure de notre code. 

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
* Main.py
* Population.py
* RotTable.py
* Traj3D.py
* Readme.md
* Rapport.md
* Requirement.txt 
* Data\
`* plasmid_8k.fasta`
`* plasmid_180k.fasta`


## Utilisation
Lancer le fichier Interface_utilisateur.py. Bien qu'assez userfriendly, aidez vous de notre 
manuel d'utilisation pour utiliser correctement notre outil. 

## Références 
[Real coded genetic algorithms (slides)](https://engineering.purdue.edu/~sudhoff/ee630/Lecture04.pdf)
[Algorithmes génétiques de Jean-Marc Alliot & Nicolas Durand](http://pom.tls.cena.fr/GA/FAG/ag.html)
[Thèse sur les jeux évolutionnaires](https://tel.archives-ouvertes.fr/tel-02085935/document)


* RotTable.py
* Traj3D.py
* Readme.md
* Rapport.md
* Requirement.txt 
* Data\
`* plasmid_8k.fasta`
`* plasmid_180k.fasta`


## Utilisation
Lancer le fichier Interface_utilisateur.py. Bien qu'assez userfriendly, aidez vous de notre 
manuel d'utilisation pour utiliser correctement notre outil. 

## Références 
[Real coded genetic algorithms (slides)](https://engineering.purdue.edu/~sudhoff/ee630/Lecture04.pdf)
[Algorithmes génétiques de Jean-Marc Alliot & Nicolas Durand](http://pom.tls.cena.fr/GA/FAG/ag.html)

