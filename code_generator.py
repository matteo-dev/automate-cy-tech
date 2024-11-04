#Génère le code C à partir des instructions 
# code_generator.py

def generate_create_cursor(tokens):
    name = tokens[1][1]
    x = tokens[3][1]
    y = tokens[4][1]
    return f"Cursor {name} = create_cursor({x}, {y});"

def generate_set_color(tokens):
    name = tokens[1][1]
    color = tokens[3][1]
    return f"set_color(&{name}, \"{color}\");"

def generate_move_cursor(tokens):
    name = tokens[1][1]
    dx = tokens[3][1]
    return f"move_cursor(&{name}, {dx});"

def generate_rotate_cursor(tokens):
    name = tokens[1][1]
    degrees = tokens[3][1]
    return f"rotate_cursor(&{name}, {degrees});"

def generate_draw_shape(tokens):
    shape = tokens[1][1]
    name = tokens[3][1]
    size = tokens[5][1]
    return f"draw_{shape}(&{name}, {size});"

def generate_code(tokens):
    if tokens[0][1] == 'cursor':
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


def generate_c_code(instructions):
    code_lines = [
        "#include <stdio.h>",
        "#include \"drawlib.h\"",
        "",
        "int main() {"
    ]

    for instruction in instructions:
        code_line = generate_code(instruction)
        code_lines.append(f"    {code_line}")

    code_lines.append("    return 0;")
    code_lines.append("}")

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

    c_code = generate_c_code(instructions)
    with open("output.c", "w") as file:
        file.write(c_code)
    print("Code C généré avec succès dans output.c")
