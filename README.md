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
- [x] Optimiser pour ne jamais muter le meilleur ; modifier tournoi (% chance gagner même si moins bon score SAUF face au meilleur)
- [x] évaluation avec scaling
- [x] Bloquer --> calcul si y'a pas de séquence et obliger les fichiers fasta 
- [x] Généraliser les vérifications des entrées des méthodes avec des raise exeception
- [x] Test et couverture des nouvelles méthodes 
- [x] changer mutate : au lieu de parcourir la liste, prendre un nb aléatoire pour nb mutations puis choisir nb mutations alétoires
- [x] établir plan du diapo 
- [x]    ordonner correctement tous les modules selon la règle suivante : 
block 1 : Import des modules présents dans python de base 
block 2 : Import de module non présent de base dans python i.e. ceux qu'on a du pip install 
block 3 : Import de fichiers propre à notre projet, ex import Traj3D
les modules au sein de chacun des blocs doivent être ordonnés par ordre alphabétique


A faire : 

- [ ] Benchmarks : sélection, évaluation, luck_prob, alpha, pertinence réduire var dans mutate
- [ ] changer évalutation prendre orientation des extrémités en compte (produit scalaire) et normes 
- [ ] Améliorations pour la présentation : pédagogie (audience novice) ; diagrammes de classe (POO) ; passer vite sur l'organisation ; être très didactique (convaincre et justifier nos choix !) ; éviter de montrer du code ; avoir des bonnes données à montrer (gros plans sur la jointure)
- [ ] Utiliser un couple d'évaluation avec 2 best à chaque génération ; on ne modifie un individu que s'il est moins bon sur les deux critères
- [ ] reprendre tous les codes, commenter proprement et virer les commentaires inutiles : 
reste à faire : genalg et main 



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
* Output\ 


## Utilisation
Lancer le fichier Interface_utilisateur.py. Bien qu'assez userfriendly, aidez vous de notre 
manuel d'utilisation pour utiliser correctement notre outil. 

## Références 
[Real coded genetic algorithms (slides)](https://engineering.purdue.edu/~sudhoff/ee630/Lecture04.pdf)
[Algorithmes génétiques de Jean-Marc Alliot & Nicolas Durand](http://pom.tls.cena.fr/GA/FAG/ag.html)
[Thèse sur les jeux évolutionnaires](https://tel.archives-ouvertes.fr/tel-02085935/document)

