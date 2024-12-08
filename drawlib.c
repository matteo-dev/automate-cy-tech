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

#include <ctype.h>

// Function to validate the color string
bool is_valid_color(const char* color) {
    if (color[0] != '#' || strlen(color) != 7) {
        return false;  // Invalid color format
    }
    for (int i = 1; i < 7; ++i) {
        if (!isxdigit(color[i])) {  // Check if each character is a valid hex digit
            return false;
        }
    }
    return true;  // Color format is valid
}

// function to set the cursor's color
bool set_color(Cursor* cursor, const char* color) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    if (!is_valid_color(color)) {
        print_error("Invalid color format");
        return false;
    }
    strcpy(cursor->color, color);  // Copy the color string into the cursor
    printf("Cursor color set to %s\n", color);  // Confirmation of the color change
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
    printf("Cursor at (%d, %d), Color: %s, Size: %d\n", cursor->x, cursor->y, cursor->color, size); //pour verifier les parametres
    printf("Drawing a circle of size %d at (%d, %d)\n", size, cursor->x, cursor->y);  // Confirmation du dessin
    return true;
}

// Function to draw a square
bool draw_square(Cursor* cursor, int size) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    if (size <= 0) {
        print_error("Invalid size for drawing");
        return false;
    }
    printf("Drawing a square of size %d at (%d, %d)\n", size, cursor->x, cursor->y);
    return true;
}

// Function to draw a rectangle
bool draw_rectangle(Cursor* cursor, int width, int height) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    if (width <= 0 || height <= 0) {
        print_error("Invalid dimensions for drawing");
        return false;
    }
    printf("Drawing a rectangle of width %d and height %d at (%d, %d)\n", width, height, cursor->x, cursor->y);
    return true;
}

// Function to draw a line
bool draw_line(Cursor* cursor, int length) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    if (length <= 0) {
        print_error("Invalid length for drawing");
        return false;
    }
    printf("Drawing a line of length %d starting at (%d, %d)\n", length, cursor->x, cursor->y);
    return true;
}

// Update draw_shape to handle new shapes
int draw_shape(const char* shape, int x, int y, int size, const char* color) {
    Cursor cursor = create_cursor(x, y);
    printf("this step is done.\n");

    if (!set_color(&cursor, color)) {
        return 2; // Error setting color
    }
    printf("Shape received: %s\n", shape);

    if (strcmp(shape, "circle") == 0) {
        return draw_circle(&cursor, size) ? 0 : 1; // Success or failure
    } else if (strcmp(shape, "square") == 0) {
        return draw_square(&cursor, size) ? 0 : 1;
    } else if (strcmp(shape, "rectangle") == 0) {
        // Example: Hardcoding height as size/2 for simplicity
        return draw_rectangle(&cursor, size, size / 2) ? 0 : 1;
    } else if (strcmp(shape, "line") == 0) {
        return draw_line(&cursor, size) ? 0 : 1;
    } else {
        printf("Shape not supported.\n");
        return 3; // Error for unsupported shape
    }
}


int main() {
    return 0;
}