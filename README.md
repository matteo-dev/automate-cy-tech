# draw++
##Exécution
 
Pour exécuter correctement l'ensemble des fonctions, il faut :

  - Télécharger l'ensemble des codes présents sur ce dépot Github et les placer dans un même répertoire
  - Installer Flask sur votre odrinateur commande pip install flask dans votre invité de commandes
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

## Auteurs

- Aicha
- Mattéo
- Ahmed
- Baptiste
- Emma
