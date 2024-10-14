#analyseur syntaxique (parsing)
class SyntaxError(Exception):
    pass

# Règle pour créer un curseur: "cursor <ID> at <NUMBER>, <NUMBER>"
def parse_create_cursor(tokens):
    if len(tokens) != 5:
        raise SyntaxError("Syntax Error: Expected 'cursor <ID> at <NUMBER>, <NUMBER>'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'cursor':
        raise SyntaxError("Syntax Error: Expected 'cursor' at the beginning")
    if tokens[1][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor name")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'at':
        raise SyntaxError("Syntax Error: Expected 'at' after cursor identifier")
    if tokens[3][0] != 'NUMBER' or tokens[4][0] != 'NUMBER':
        raise SyntaxError("Syntax Error: Expected two numbers for the position")
    return True

# Règle pour affecter une couleur: "set <ID> color <COLOR>"
def parse_set_color(tokens):
    if len(tokens) != 4:
        raise SyntaxError("Syntax Error: Expected 'set <ID> color <COLOR>'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'set':
        raise SyntaxError("Syntax Error: Expected 'set' at the beginning")
    if tokens[1][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'color':
        raise SyntaxError("Syntax Error: Expected 'color' after identifier")
    if tokens[3][0] != 'COLOR':
        raise SyntaxError("Syntax Error: Expected a valid color")
    return True

# Règle pour affecter une épaisseur: "set <ID> thickness <NUMBER>"
def parse_set_thickness(tokens):
    if len(tokens) != 4:
        raise SyntaxError("Syntax Error: Expected 'set <ID> thickness <NUMBER>'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'set':
        raise SyntaxError("Syntax Error: Expected 'set' at the beginning")
    if tokens[1][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'thickness':
        raise SyntaxError("Syntax Error: Expected 'thickness' after identifier")
    if tokens[3][0] != 'NUMBER':
        raise SyntaxError("Syntax Error: Expected a valid number for thickness")
    return True

# Règle pour déplacer un curseur: "move <ID> by <NUMBER>"
def parse_move_cursor(tokens):
    if len(tokens) != 4:
        raise SyntaxError("Syntax Error: Expected 'move <ID> by <NUMBER>'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'move':
        raise SyntaxError("Syntax Error: Expected 'move' at the beginning")
    if tokens[1][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'by':
        raise SyntaxError("Syntax Error: Expected 'by' after identifier")
    if tokens[3][0] != 'NUMBER':
        raise SyntaxError("Syntax Error: Expected a valid number for movement")
    return True

# Règle pour faire pivoter un curseur: "rotate <ID> by <NUMBER> degrees"
def parse_rotate_cursor(tokens):
    if len(tokens) != 6:
        raise SyntaxError("Syntax Error: Expected 'rotate <ID> by <NUMBER> degrees'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'rotate':
        raise SyntaxError("Syntax Error: Expected 'rotate' at the beginning")
    if tokens[1][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'by':
        raise SyntaxError("Syntax Error: Expected 'by' after identifier")
    if tokens[3][0] != 'NUMBER':
        raise SyntaxError("Syntax Error: Expected a valid number for rotation")
    if tokens[4][0] != 'KEYWORD' or tokens[4][1] != 'degrees':
        raise SyntaxError("Syntax Error: Expected 'degrees' after number")
    return True

# Règle pour dessiner une forme: "draw <SHAPE> with <ID> size <NUMBER>"
def parse_draw_shape(tokens):
    if len(tokens) != 6:
        raise SyntaxError("Syntax Error: Expected 'draw <SHAPE> with <ID> size <NUMBER>'")
    if tokens[0][0] != 'KEYWORD' or tokens[0][1] != 'draw':
        raise SyntaxError("Syntax Error: Expected 'draw' at the beginning")
    if tokens[1][0] != 'SHAPE':
        raise SyntaxError("Syntax Error: Expected a valid shape after 'draw'")
    if tokens[2][0] != 'KEYWORD' or tokens[2][1] != 'with':
        raise SyntaxError("Syntax Error: Expected 'with' after shape")
    if tokens[3][0] != 'IDENTIFIER':
        raise SyntaxError("Syntax Error: Expected identifier for cursor")
    if tokens[4][0] != 'KEYWORD' or tokens[4][1] != 'size':
        raise SyntaxError("Syntax Error: Expected 'size' after identifier")
    if tokens[5][0] != 'NUMBER':
        raise SyntaxError("Syntax Error: Expected a valid number for size")
    return True

# Fonction principale de parsing, qui appelle les règles spécifiques en fonction de l'instruction
def parse(tokens):
    if not tokens:
        return
    if tokens[0][1] == 'cursor':
        return parse_create_cursor(tokens)
    elif tokens[0][1] == 'set' and tokens[2][1] == 'color':
        return parse_set_color(tokens)
    elif tokens[0][1] == 'set' and tokens[2][1] == 'thickness':
        return parse_set_thickness(tokens)
    elif tokens[0][1] == 'move':
        return parse_move_cursor(tokens)
    elif tokens[0][1] == 'rotate':
        return parse_rotate_cursor(tokens)
    elif tokens[0][1] == 'draw':
        return parse_draw_shape(tokens)
    else:
        raise SyntaxError(f"Syntax Error: Unknown instruction '{tokens[0][1]}'")
