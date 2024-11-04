#ifndef DRAWLIB_H
#define DRAWLIB_H

#include <stdbool.h>

typedef struct {
    char name[50];
    int x;
    int y;
    char color[20];
    int thickness;
    bool initialized;
} Cursor;

// Déclarations des fonctions
Cursor create_cursor(int x, int y);
bool set_color(Cursor* cursor, const char* color);
bool move_cursor(Cursor* cursor, int dx);
bool rotate_cursor(Cursor* cursor, int degrees);
bool draw_circle(Cursor* cursor, int size);

// Fonction pour afficher un message d'erreur
void print_error(const char* message);

#endif // DRAWLIB_H
