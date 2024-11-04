#include <stdio.h>
#include <string.h>
#include "drawlib.h"

// Implémentation des fonctions
Cursor create_cursor(int x, int y) {
    Cursor c;
    strcpy(c.name, "default");
    c.x = x;
    c.y = y;
    strcpy(c.color, "black");
    c.thickness = 1;
    printf("Cursor created at (%d, %d)\n", x, y);
    return c;
}

void set_color(Cursor* cursor, const char* color) {
    strcpy(cursor->color, color);
    printf("Cursor color set to %s\n", color);
}

void move_cursor(Cursor* cursor, int dx) {
    cursor->x += dx;
    printf("Cursor moved to (%d, %d)\n", cursor->x, cursor->y);
}

void rotate_cursor(Cursor* cursor, int degrees) {
    printf("Cursor rotated by %d degrees\n", degrees);
}

void draw_circle(Cursor* cursor, int size) {
    printf("Drawing a circle of size %d at (%d, %d)\n", size, cursor->x, cursor->y);
}
