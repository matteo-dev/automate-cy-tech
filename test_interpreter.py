from interpreter import interpret

# Liste des instructions draw++ après parsing (tokens)
instructions = [
    [('KEYWORD', 'cursor'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'at'), ('NUMBER', '100'), ('NUMBER', '150')],
    [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'color'), ('COLOR', 'red')],
    [('KEYWORD', 'move'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '50')],
    [('KEYWORD', 'rotate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '90'), ('KEYWORD', 'degrees')],
    [('KEYWORD', 'draw'), ('SHAPE', 'circle'), ('KEYWORD', 'with'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'size'), ('NUMBER', '30')],
    [('KEYWORD', 'animate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'with'), ('KEYWORD', 'rotate'), ('KEYWORD', 'for'), ('NUMBER', '5')],
    [('KEYWORD', 'animate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'with'), ('KEYWORD', 'move'), ('KEYWORD', 'for'), ('NUMBER', '5')],
]

# Exécution des instructions
for instruction in instructions:
    interpret(instruction)
