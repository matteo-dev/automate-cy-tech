import tkinter as tk
from tkinter import Canvas

class DrawApp:
    def __init__(self, master):
        # Initialisation de la fenêtre principale
        self.master = master
        self.master.title("draw++ Visualizer")
        
        # Création d'un canevas pour dessiner
        self.canvas = Canvas(master, width=800, height=600, bg="white")
        self.canvas.pack()  # Placement du canevas

    # Méthode pour dessiner un cercle
    def draw_circle(self, x, y, size, color="black"):
        self.canvas.create_oval(x - size, y - size, x + size, y + size, outline=color, width=2)

    # Méthode pour dessiner un carré
    def draw_square(self, x, y, size, color="black"):
        self.canvas.create_rectangle(x - size, y - size, x + size, y + size, outline=color, width=2)

    # Méthode pour déplacer un curseur
    def move_cursor(self, cursor, dx, dy):
        cursor['x'] += dx  # Mise à jour de la position x
        cursor['y'] += dy  # Mise à jour de la position y

    # Méthode pour tourner un curseur (symbolique, sans effet visible sur l'UI)
    def rotate_cursor(self, cursor, degrees):
        pass  # Rotation non implémentée pour l'UI

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()  # Création de la fenêtre principale
    app = DrawApp(root)

    # Exemple de dessin sur le canevas
    app.draw_circle(100, 100, 30, "red")  # Dessine un cercle rouge
    app.draw_square(200, 200, 50, "blue")  # Dessine un carré bleu

    root.mainloop()  # Lance la boucle principale de l'interface
