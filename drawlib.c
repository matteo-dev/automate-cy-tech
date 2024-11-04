#include <stdio.h>
#include <string.h>
#include "drawlib.h"

void print_error(const char* message) {
    fprintf(stderr, "Error: %s\n", message);
}

Cursor create_cursor(int x, int y) {
    Cursor c;
    strcpy(c.name, "default");
    c.x = x;
    c.y = y;
    strcpy(c.color, "black");
    c.thickness = 1;
    c.initialized = true;
    printf("Cursor created at (%d, %d)\n", x, y);
    return c;
}

bool set_color(Cursor* cursor, const char* color) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    strcpy(cursor->color, color);
    printf("Cursor color set to %s\n", color);
    return true;
}

bool move_cursor(Cursor* cursor, int dx) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    cursor->x += dx;
    printf("Cursor moved to (%d, %d)\n", cursor->x, cursor->y);
    return true;
}

bool rotate_cursor(Cursor* cursor, int degrees) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    printf("Cursor rotated by %d degrees\n", degrees);
    return true;
}

bool draw_circle(Cursor* cursor, int size) {
    if (!cursor->initialized) {
        print_error("Cursor not initialized");
        return false;
    }
    if (size <= 0) {
        print_error("Invalid size for drawing");
        return false;
    }
    printf("Drawing a circle of size %d at (%d, %d)\n", size, cursor->x, cursor->y);
    return true;
}
