# Classe pour gérer les erreurs de syntaxe personnalisées
class SyntaxError(Exception):
    pass

# Analyse de la structure d'une instruction "if"
def parse_if_statement(tokens):
    # Exemple de structure : "if <CONDITION> { <BLOC_D'INSTRUCTIONS> }"
    if tokens[0][1] != 'if' or tokens[1][0] != 'CONDITION':
        raise SyntaxError("Syntax Error: Expected 'if <CONDITION> { ... }'")
    # Ici, la logique pour analyser un bloc d'instructions peut être ajoutée
    return True

# Analyse de la structure d'une boucle "while"
def parse_while_loop(tokens):
    # Exemple de structure : "while <CONDITION> { <BLOC_D'INSTRUCTIONS> }"
    if tokens[0][1] != 'while' or tokens[1][0] != 'CONDITION':
        raise SyntaxError("Syntax Error: Expected 'while <CONDITION> { ... }'")
    return True

# Analyse de l'instruction pour créer un curseur : "cursor <ID> at <NUMBER>, <NUMBER>"
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

# Analyse de l'instruction pour définir une couleur : "set <ID> color <COLOR>"
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

# Analyse de l'instruction pour définir l'épaisseur : "set <ID> thickness <NUMBER>"
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

# Analyse de l'instruction pour déplacer un curseur : "move <ID> by <NUMBER>"
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

# Analyse de l'instruction pour faire pivoter un curseur : "rotate <ID> by <NUMBER> degrees"
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

# Analyse de l'instruction pour dessiner une forme : "draw <SHAPE> with <ID> size <NUMBER>"
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

# Fonction principale de parsing qui appelle les règles spécifiques en fonction de l'instruction
def parse(tokens):
    if not tokens:
        return
    if tokens[0][1] == 'if':
        return parse_if_statement(tokens)
    elif tokens[0][1] == 'for':
        return parse_for_loop(tokens)
    elif tokens[0][1] == 'while':
        return parse_while_loop(tokens)
    elif tokens[0][1] == 'cursor':
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


# Classe pour gérer les erreurs de syntaxe personnalisées
class SyntaxError(Exception):
    pass

# Analyse de la structure d'une boucle "for"
def parse_for_loop(tokens, index):
    if len(tokens) <= index + 6:
        raise SyntaxError("Invalid 'for' loop syntax. Expected: 'for <var> from <start> to <end> { ... }'")

    # Ensure correct sequence: for <var> from <start> to <end> {
    if tokens[index][1] != 'for' or tokens[index + 2][1] != 'from' or tokens[index + 4][1] != 'to':
        raise SyntaxError("Invalid 'for' loop syntax. Missing 'from' or 'to'.")

    variable = tokens[index + 1][1]  # Variable name
    start = int(tokens[index + 3][1])  # Start value
    end = int(tokens[index + 5][1])  # End value

    # Ensure '{' follows the loop header
    if tokens[index + 6][0] != 'OPEN_BRACE':
        raise SyntaxError("Expected '{' after 'for' loop header.")

    # Extract loop body
    body_tokens = []
    loop_index = index + 7
    while loop_index < len(tokens) and tokens[loop_index][0] != 'CLOSE_BRACE':
        body_tokens.append(tokens[loop_index])
        loop_index += 1

    if loop_index == len(tokens):
        raise SyntaxError("Expected '}' to close 'for' loop body.")

    # Parse the body commands
    body_commands = parse_commands(body_tokens)

    # Generate loop structure
    return {
        "type": "for",
        "variable": variable,
        "start": start,
        "end": end,
        "body": body_commands,
    }, loop_index

# Analyse de la structure d'une boucle "while"
def parse_while_loop(tokens, index):
    if len(tokens) <= index + 2:
        raise SyntaxError("Invalid 'while' loop syntax. Expected: 'while <condition> { ... }'")

    # Ensure correct structure: while <condition> {
    if tokens[index][1] != 'while' or tokens[index + 1][0] != 'CONDITION' or tokens[index + 2][0] != 'OPEN_BRACE':
        raise SyntaxError("Invalid 'while' loop syntax or missing '{'.")

    condition = tokens[index + 1][1]  # The condition string

    # Extract loop body
    body_tokens = []
    loop_index = index + 3
    while loop_index < len(tokens) and tokens[loop_index][0] != 'CLOSE_BRACE':
        body_tokens.append(tokens[loop_index])
        loop_index += 1

    if loop_index == len(tokens):
        raise SyntaxError("Expected '}' to close 'while' loop body.")

    # Parse the body commands
    body_commands = parse_commands(body_tokens)

    # Generate loop structure
    return {
        "type": "while",
        "condition": condition,
        "body": body_commands,
    }, loop_index

# Fonction principale de parsing qui appelle les règles spécifiques en fonction de l'instruction
def parse_commands(tokens):
    commands = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token[1] == 'for':  # Detect 'for' loops
            loop_command, i = parse_for_loop(tokens, i)
            commands.append(loop_command)
        elif token[1] == 'while':  # Detect 'while' loops
            loop_command, i = parse_while_loop(tokens, i)
            commands.append(loop_command)
        elif token[1] == 'draw':  # Example for drawing commands
            draw_command, i = parse_draw_command(tokens, i)
            commands.append(draw_command)
        else:
            raise SyntaxError(f"Unknown command: {token[1]} at position {i}")
        i += 1

    return commands

# Analyse de l'instruction pour dessiner une forme : "draw <SHAPE> size <NUMBER>"
def parse_draw_command(tokens, index):
    if len(tokens) <= index + 2 or tokens[index][1] != 'draw' or tokens[index + 2][0] != 'NUMBER':
        raise SyntaxError(f"Invalid 'draw' command syntax at token {index}.")

    shape = tokens[index + 1][1]  # Shape name
    size = int(tokens[index + 2][1])  # Shape size

    return {"type": "draw", "shape": shape, "size": size}, index + 2

def parse_body(tokens):
    """
    Parse a block of tokens inside a loop or condition.
    """
    commands = []
    for token in tokens:
        if token[1] == 'circle':  # Example: Parse 'circle' commands
            commands.append({"type": "draw", "shape": "circle", "size": int(tokens[1][1])})
        elif token[1] == 'line':  # Example: Parse 'line' commands
            commands.append({"type": "draw", "shape": "line", "length": int(tokens[1][1])})
        # Add parsing logic for other commands here
        else:
            raise SyntaxError(f"Unknown command in body: {token[1]}")
    return commands
