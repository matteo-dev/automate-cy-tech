#include <stdio.h>
#include "drawlib.h"

int main() {
    Cursor C1 = create_cursor(100, 150);
    if (!set_color(&C1, "red");) { return 1; }
    if (!move_cursor(&C1, 50);) { return 1; }
    if (!rotate_cursor(&C1, 90);) { return 1; }
    if (!draw_circle(&C1, 30);) { return 1; }
    return 0;
}