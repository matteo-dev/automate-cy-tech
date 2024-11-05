#ifndef DRAWLIB_H
#define DRAWLIB_H

#include <stdbool.h>

// Définition de la structure Cursor
typedef struct {
    char name[50];       // Nom du curseur
    int x;               // Position x du curseur
    int y;               // Position y du curseur
    char color[20];      // Couleur du curseur
    int thickness;       // Épaisseur du curseur
    bool initialized;    // Indicateur d'initialisation
} Cursor;

// Déclarations des fonctions pour manipuler un curseur

// Fonction pour créer un curseur à une position donnée
Cursor create_cursor(int x, int y);

// Fonction pour définir la couleur d'un curseur
bool set_color(Cursor* cursor, const char* color);

// Fonction pour déplacer un curseur d'une distance donnée
bool move_cursor(Cursor* cursor, int dx);

// Fonction pour faire tourner un curseur d'un certain nombre de degrés
bool rotate_cursor(Cursor* cursor, int degrees);

// Fonction pour dessiner un cercle avec un curseur
bool draw_circle(Cursor* cursor, int size);

// Fonction pour afficher un message d'erreur
void print_error(const char* message);

#endif // DRAWLIB_H
