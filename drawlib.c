#include <stdio.h>
#include <string.h>
#include "drawlib.h"

// Fonction pour imprimer un message d'erreur
void print_error(const char* message) {
    fprintf(stderr, "Error: %s\n", message);
}

// Fonction pour créer un curseur à une position donnée
Cursor create_cursor(int x, int y) {
    Cursor c;  // Déclaration du curseur
    strcpy(c.name, "default");  // Nom par défaut du curseur
    c.x = x;  // Position x initiale
    c.y = y;  // Position y initiale
    strcpy(c.color, "black");  // Couleur par défaut du curseur
    c.thickness = 1;  // Épaisseur par défaut
    c.initialized = true;  // Le curseur est initialisé
    printf("Cursor created at (%d, %d)\n", x, y);  // Confirmation de la création
    return c;  // Retourne le curseur créé
}

// Fonction pour définir la couleur d'un curseur
bool set_color(Cursor* cursor, const char* color) {
    if (!cursor->initialized) {  // Vérifie si le curseur est initialisé
        print_error("Cursor not initialized");
        return false;
    }
    strcpy(cursor->color, color);  // Change la couleur du curseur
    printf("Cursor color set to %s\n", color);  // Confirmation du changement de couleur
    return true;
}

// Fonction pour déplacer un curseur d'une distance dx
bool move_cursor(Cursor* cursor, int dx) {
    if (!cursor->initialized) {  // Vérifie si le curseur est initialisé
        print_error("Cursor not initialized");
        return false;
    }
    cursor->x += dx;  // Déplace le curseur sur l'axe x
    printf("Cursor moved to (%d, %d)\n", cursor->x, cursor->y);  // Confirmation du déplacement
    return true;
}

// Fonction pour faire tourner un curseur d'un certain nombre de degrés
bool rotate_cursor(Cursor* cursor, int degrees) {
    if (!cursor->initialized) {  // Vérifie si le curseur est initialisé
        print_error("Cursor not initialized");
        return false;
    }
    printf("Cursor rotated by %d degrees\n", degrees);  // Confirmation de la rotation
    return true;
}

// Fonction pour dessiner un cercle avec un curseur
bool draw_circle(Cursor* cursor, int size) {
    if (!cursor->initialized) {  // Vérifie si le curseur est initialisé
        print_error("Cursor not initialized");
        return false;
    }
    if (size <= 0) {  // Vérifie si la taille est valide
        print_error("Invalid size for drawing");
        return false;
    }
    printf("Drawing a circle of size %d at (%d, %d)\n", size, cursor->x, cursor->y);  // Confirmation du dessin
    return true;
}

int main() {
    return 0;
}