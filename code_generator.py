# code_generator.py
# Initialiser l'interface
from interpreter import interpret
import time
import tkinter as tk
from interface import DrawApp  # Assure-toi que DrawApp est dans un fichier nommé interface.py

# Création de la fenêtre principale de l'application
root = tk.Tk()
app = DrawApp(root)

# Génère le code C pour une instruction "if"
def generate_if_statement(tokens):
    condition = tokens[1][1]  # Récupérer la condition
    return f"if ({condition}) {{\n    // Code généré pour le bloc\n}}"

# Génère le code C pour une boucle "for"
def generate_for_loop(tokens):
    var_name = tokens[1][1]
    start = tokens[3][1]
    end = tokens[5][1]
    return f"for (int {var_name} = {start}; {var_name} <= {end}; {var_name}++) {{\n    // Code généré pour le bloc\n}}"

# Génère le code C pour une boucle "while"
def generate_while_loop(tokens):
    condition = tokens[1][1]
    return f"while ({condition}) {{\n    // Code généré pour le bloc\n}}"

# Génère le code C pour la création d'un curseur
def generate_create_cursor(tokens):
    name = tokens[1][1]
    x = tokens[3][1]
    y = tokens[4][1]
    return f"Cursor {name} = create_cursor({x}, {y});"

# Génère le code C pour définir la couleur d'un curseur
def generate_set_color(tokens):
    name = tokens[1][1]
    color = tokens[3][1]
    return f"set_color(&{name}, \"{color}\");"

# Génère le code C pour déplacer un curseur
def generate_move_cursor(tokens):
    name = tokens[1][1]
    dx = tokens[3][1]
    return f"move_cursor(&{name}, {dx});"

# Génère le code C pour faire tourner un curseur
def generate_rotate_cursor(tokens):
    name = tokens[1][1]
    degrees = tokens[3][1]
    return f"rotate_cursor(&{name}, {degrees});"

# Génère le code C pour dessiner une forme
def generate_draw_shape(tokens):
    shape = tokens[1][1]
    name = tokens[3][1]
    size = tokens[5][1]
    return f"draw_{shape}(&{name}, {size});"

# Génère le code C en fonction du type d'instruction
def generate_code(tokens):
    if tokens[0][1] == 'if':
        return generate_if_statement(tokens)
    elif tokens[0][1] == 'for':
        return generate_for_loop(tokens)
    elif tokens[0][1] == 'while':
        return generate_while_loop(tokens)
    elif tokens[0][1] == 'cursor':
        return generate_create_cursor(tokens)
    elif tokens[0][1] == 'set' and tokens[2][1] == 'color':
        return f"if (!{generate_set_color(tokens)}) {{ return 1; }}"
    elif tokens[0][1] == 'move':
        return f"if (!{generate_move_cursor(tokens)}) {{ return 1; }}"
    elif tokens[0][1] == 'rotate':
        return f"if (!{generate_rotate_cursor(tokens)}) {{ return 1; }}"
    elif tokens[0][1] == 'draw':
        return f"if (!{generate_draw_shape(tokens)}) {{ return 1; }}"
    else:
        raise ValueError(f"Unknown instruction: {tokens[0][1]}")

# Génère le code C à partir d'une liste d'instructions
def generate_c_code(instructions):
    code_lines = [
        "#include <stdio.h>",
        "#include \"drawlib.h\"",
        "",
        "int main() {"
    ]

    # Ajouter chaque ligne de code générée à la liste
    for instruction in instructions:
        code_line = generate_code(instruction)
        code_lines.append(f"    {code_line}")

    # Ajouter la fin de la fonction main
    code_lines.append("    return 0;")
    code_lines.append("}")

    # Retourner le code complet
    return "\n".join(code_lines)

# Exemple de sauvegarde dans un fichier
if __name__ == "__main__":
    instructions = [
        [('KEYWORD', 'cursor'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'at'), ('NUMBER', '100'), ('NUMBER', '150')],
        [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'color'), ('COLOR', 'red')],
        [('KEYWORD', 'move'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '50')],
        [('KEYWORD', 'rotate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '90'), ('KEYWORD', 'degrees')],
        [('KEYWORD', 'draw'), ('SHAPE', 'circle'), ('KEYWORD', 'with'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'size'), ('NUMBER', '30')],
    ]

    # Exécuter l'interprétation des instructions
    for instruction in instructions:
        interpret(instruction)

    # Lancer l'interface graphique
    root.mainloop()

    # Générer et sauvegarder le code C
    c_code = generate_c_code(instructions)
    with open("output.c", "w") as file:
        file.write(c_code)
    print("Code C généré avec succès dans output.c")

def generate_for_loop(loop):
    return f"for (int {loop['variable']} = {loop['start']}; {loop['variable']} <= {loop['end']}; {loop['variable']}++) {{\n" \
           + "\n".join(generate_code(cmd) for cmd in loop['body']) + "\n}"

def generate_while_loop(loop):
    return f"while ({loop['condition']}) {{\n" \
           + "\n".join(generate_code(cmd) for cmd in loop['body']) + "\n}"
