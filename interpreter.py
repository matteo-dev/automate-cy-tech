#interprète du langage draw++
import time
import tkinter as tk
from  interface import DrawApp  # Assure-toi que DrawApp est dans un fichier nommé draw_ui.py

# Initialiser l'interface
root = tk.Tk()
app = DrawApp(root)

# Classe pour représenter un curseur avec position, couleur et épaisseur
class Cursor:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.color = 'black'
        self.thickness = 1

    def move(self, dx):
        self.x += dx
        print(f"{self.name} moved to ({self.x}, {self.y})")

    def rotate(self, degrees):
        print(f"{self.name} rotated by {degrees} degrees")

    def set_color(self, color):
        self.color = color
        print(f"{self.name} color set to {self.color}")

    def set_thickness(self, thickness):
        self.thickness = thickness
        print(f"{self.name} thickness set to {self.thickness}")

    def draw_shape(self, shape, size):
        print(f"{self.name} drew a {shape} of size {size} at ({self.x}, {self.y})")


# Fonction d'animation pour la rotation
def animate_rotation(cursor, degrees, duration):
    steps = 10  # Diviser l'animation en 10 étapes
    degrees_per_step = degrees / steps
    time_per_step = duration / steps

    for _ in range(steps):
        cursor.rotate(degrees_per_step)
        time.sleep(time_per_step)


# Fonction d'animation pour le mouvement
def animate_movement(cursor, distance, duration):
    steps = 10  # Diviser l'animation en 10 étapes
    distance_per_step = distance / steps
    time_per_step = duration / steps

    for _ in range(steps):
        cursor.move(distance_per_step)
        time.sleep(time_per_step)


# Dictionnaire pour stocker les curseurs créés
cursors = {}

# Fonction principale d'interprétation
def interpret(tokens):
    if tokens[0][1] == 'draw' and tokens[1][1] == 'circle':
        x, y = 150, 150  # Remplacer par la position du curseur si nécessaire
        size = int(tokens[5][1])
        app.draw_circle(x, y, size, "black")

    elif tokens[0][1] == 'draw' and tokens[1][1] == 'square':
        x, y = 200, 200  # Position par défaut ou calculée
        size = int(tokens[5][1])
        app.draw_square(x, y, size, "blue")

    # Autres instructions draw++ à intégrer

    # Pour gérer le mouvement, modifier la position et mettre à jour l'affichage
    elif tokens[0][1] == 'move':
        dx = int(tokens[3][1])
        cursor = {'x': 150, 'y': 150}  # Exemple de curseur
        app.move_cursor(cursor, dx, 0)  # Déplacement uniquement horizontal pour cet exemple

    if tokens[0][1] == 'cursor':
        name = tokens[1][1]
        x, y = int(tokens[3][1]), int(tokens[4][1])
        cursors[name] = Cursor(name, x, y)
        print(f"Cursor {name} created at ({x}, {y})")

    
    elif tokens[0][1] == 'if':
        condition = tokens[1][1]  # Exemple de récupération de la condition
        if evaluate_condition(condition):  # Implémente la fonction `evaluate_condition`
            # Exécuter le bloc d'instructions
            interpret_block(tokens[3:])  # Fonction pour exécuter un bloc d'instructions

    elif tokens[0][1] == 'for':
        var_name = tokens[1][1]
        start = int(tokens[3][1])
        end = int(tokens[5][1])
        for i in range(start, end + 1):
            interpret_block(tokens[7:])  # Exécuter le bloc d'instructions

    elif tokens[0][1] == 'while':
        condition = tokens[1][1]
        while evaluate_condition(condition):  # Boucle tant que la condition est vraie
            interpret_block(tokens[3:])
            
    elif tokens[0][1] == 'move':
        name = tokens[1][1]
        dx = int(tokens[3][1])
        cursors[name].move(dx)

    elif tokens[0][1] == 'rotate':
        name = tokens[1][1]
        degrees = int(tokens[3][1])
        cursors[name].rotate(degrees)

    elif tokens[0][1] == 'set' and tokens[2][1] == 'color':
        name = tokens[1][1]
        color = tokens[3][1]
        cursors[name].set_color(color)

    elif tokens[0][1] == 'set' and tokens[2][1] == 'thickness':
        name = tokens[1][1]
        thickness = int(tokens[3][1])
        cursors[name].set_thickness(thickness)

    elif tokens[0][1] == 'draw':
        shape = tokens[1][1]
        name = tokens[3][1]
        size = int(tokens[5][1])
        cursors[name].draw_shape(shape, size)

    # Ajout de l'instruction "animate"
    elif tokens[0][1] == 'animate':
        name = tokens[1][1]
        action = tokens[3][1]  # Action à animer (rotate, move, etc.)
        duration = int(tokens[5][1])  # Durée de l'animation en secondes

        if action == 'rotate':
            degrees = 360  # Exemple de rotation complète
            animate_rotation(cursors[name], degrees, duration)

        elif action == 'move':
            distance = 100  # Exemple de distance
            animate_movement(cursors[name], distance, duration)

    else:
        raise ValueError(f"Unknown instruction: {tokens[0][1]}")

def interpret_block(block_tokens):
    for instruction in block_tokens:
        interpret(instruction)

def interpret_with_ui(app, tokens):
    if tokens[0][1] == 'draw' and tokens[1][1] == 'circle':
        x, y = 150, 150  # Position par défaut ou calculée
        size = int(tokens[5][1])
        app.draw_circle(x, y, size, "black")
