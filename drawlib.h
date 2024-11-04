#ifndef DRAWLIB_H
#define DRAWLIB_H

typedef struct {
    char name[50];
    int x;
    int y;
    char color[20];
    int thickness;
} Cursor;

// Déclarations des fonctions
Cursor create_cursor(int x, int y);
void set_color(Cursor* cursor, const char* color);
void move_cursor(Cursor* cursor, int dx);
void rotate_cursor(Cursor* cursor, int degrees);
void draw_circle(Cursor* cursor, int size);
// Ajouter d'autres fonctions pour d'autres formes

#endif // DRAWLIB_H
