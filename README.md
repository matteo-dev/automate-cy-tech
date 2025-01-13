# draw++

## Exécution
 
Pour exécuter correctement l'ensemble des fonctions, il faut :

  - Télécharger l'ensemble des codes présents sur ce dépot Github et les placer dans un même répertoire
  - Installer Flask sur votre odrinateur commande pip install flask dans votre terminal
  - Exécuter le code python app.py

## Description

**draw++** est un langage de programmation graphique conçu pour dessiner et manipuler des formes sur un écran via des instructions simples et avancées. Ce projet vise à développer un environnement de développement intégré (IDE), un compilateur en Python, et un code intermédiaire en C pour exécuter des programmes écrits dans ce langage.

Le projet est réalisé dans le cadre d'un apprentissage en ING1 Génie Mathématique, avec une équipe de 4 à 5 personnes.

## Fonctionnalités

- **Langage de programmation graphique** avec des instructions élémentaires (déplacement, dessin de formes) et avancées (conditions, boucles, variables).
- **IDE intégré** permettant d'écrire, d'exécuter et de visualiser les programmes `draw++`.
- **Compilateur en Python** qui traduit le code `draw++` en un code intermédiaire C.
- **Système de correction d'erreurs** intégré pour aider à identifier et corriger les erreurs de syntaxe dans les programmes.

## Instructions 

- Créer un curseur. Vous pouvez en avoir plusieurs. Un curseur a une position actuelle sur
l’écran, souvent représentée par des coordonnées (x, y). Il peut être visible ou non sur l’écran.
- Affecter une couleur ou une épaisseur à un curseur.
- Faire avancer (un saut) un curseur de manière relative exprimée en pixels.
- Faire pivoter un curseur d’une quantité relative exprimée en degrés.
- Dessiner, pour un curseur donné, une forme (segment, carrée, cercle, point, arc, ...). Les caractéristiquesdes formes doivent être spécifiées comme opérandes des instructions.
- Animer un dessin.
- Et d’autres instructions à proposer.

- Instruction d’assignation : Affectation de valeurs à des variables .
- Instructions de Bloc : Regroupement d’instructions en une seule unité.
- Instructions Conditionnelles : if, else pour exécuter du code en fonction de conditions.
- Instructions Répétitives : Boucles for, while, do-while pour répéter des instructions plusieurs
fois.

## Listes des tokens 

a. Mots-clés
Ces mots-clés sont réservés et ont une signification particulière dans le langage.
- cursor : pour créer un curseur.
- move : pour déplacer un curseur.
- rotate : pour faire pivoter un curseur.
- set : pour affecter une couleur ou une épaisseur.
- draw : pour dessiner une forme.
- animate : pour animer un dessin.
- if, else : pour les conditions.
- for, while : pour les boucles.
- begin, end : pour délimiter des blocs d'instructions.
- to : utilisé dans les boucles for.
- color, thickness, size : pour définir des propriétés.
  
b. Symboles
Ce sont les opérateurs et séparateurs utilisés pour structurer le code.
- = : opérateur d'assignation.
- +, -, *, / : opérateurs arithmétiques.
- <, >, == : opérateurs de comparaison.
- , : séparateur pour les coordonnées ou paramètres.
- (, ) : parenthèses pour regrouper des expressions.
- {, } : accolades pour les blocs d'instructions.
- : : souvent utilisé pour la syntaxe conditionnelle.
- c. Identifiants
  
Noms de curseurs ou de variables définis par l'utilisateur.
Exemple : C1, x, y.

d. Littéraux
Ce sont les valeurs numériques ou les valeurs de propriété qui peuvent apparaître dans les instructions.
- Nombres : entiers pour les coordonnées, tailles, etc.
- Couleurs : noms de couleurs prédéfinies (red, blue, green, etc.).

e. Formes
- Ces tokens représentent les différentes formes à dessiner : segment, circle, square, arc, point.

## Fichiers principaux

Structure du Projet

Voici un aperçu des fichiers principaux du projet :

Fichiers Principaux

1. app.py

Ce fichier est le point d'entrée principal du projet. Il initialise le programme et gère l'exécution principale en coordonnant les autres modules.

2. parser.py

Implémente un analyseur syntaxique (parser) pour vérifier et structurer les entrées selon les règles définies par le langage cible.

3. lexer.py

Ce module implémente l'analyseur lexical (lexer), divisant l'entrée en unités lexicales ou "tokens".

4. interpreter.py

Ce module prend le code analysé et l'exécute en suivant les règles définies pour interpréter le langage cible.

5. code_generator.py

Génère du code ou des instructions basées sur les données analysées par le parser.

6. shapes.py

Contient des fonctions utilitaires ou des classes utilisées dans d'autres modules.

7. interface.py

Fournit une interface utilisateur pour interagir avec le système.

8. errod_handling.py

Gère les erreurs rencontrées lors du lexing, parsing ou de l'interprétation.

## Installation necesssaires 

Prérequis

Python 3.x

Modules listés dans requirements.txt

Étapes d'installation

Cloner le dépôt :

git clone https://github.com/matteo-dev/automate-cy-tech.git

Naviguer dans le répertoire du projet :

cd automate-cy-tech

Installer les dépendances :

pip install -r requirements.txt

## Comment utiliser 

Utilisation

Commandes principales

Pour exécuter le programme principal :

python app.py

Pour exécuter les tests :

python -m unittest discover

Exemples :

voir la video et aller a la toute fin!

## Configuration

Fichiers VSCode

Des fichiers dans .vscode/ sont inclus pour configurer l'environnement de développement avec VSCode, comme settings.json, launch.json, et tasks.json.

## Comment Contribuer

Étapes pour contribuer

Forkez le dépôt.

Créez une branche pour votre fonctionnalité :

git checkout -b ma-nouvelle-fonctionnalite

Faites vos modifications et ajoutez-les :

git add .

Commitez vos changements :

git commit -m "Ajout d'une nouvelle fonctionnalité"

Poussez votre branche :

git push origin ma-nouvelle-fonctionnalite

Ouvrez une Pull Request.

## Auteurs

- Aicha
- Mattéo
- Ahmed
- Baptiste
- Emma
