import tkinter as tk
from tkinter import Canvas

class DrawApp:
    def __init__(self, master):
        self.master = master
        self.master.title("draw++ Visualizer")
        self.canvas = Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()

    def draw_circle(self, x, y, size, color="black"):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=2)

    def draw_square(self, x, y, size, color="black"):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=2)

    def move_cursor(self, cursor, dx, dy):
        cursor['x'] += dx
        cursor['y'] += dy

    def rotate_cursor(self, cursor, degrees):
        # Rotation pour l'instant symbolique, non visible sur l'UI.
        pass

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)

    # Exemple de dessin
    app.draw_circle(100, 100, 30, "red")
    app.draw_square(200, 200, 50, "blue")

    root.mainloop()
