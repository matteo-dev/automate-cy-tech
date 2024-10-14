#analyseur lexical (tokenisation)
import re

# Définition des regex pour les différents types de tokens
TOKENS = [
    ('KEYWORD', r'\b(cursor|move|draw|set|if|else|for|while|color|thickness|size|animate|rotate|degrees|by)\b'),
    ('NUMBER', r'\b\d+\b'),                       # Nombres
    ('COLOR', r'\b(red|blue|green|black)\b'),     # Couleurs prédéfinies
    ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'), # Identifiants pour variables et curseurs
    ('SYMBOL', r'[=+*/<>(){}:,]'),                # Symboles divers
    ('WHITESPACE', r'\s+'),                       # Espaces et tabulations
    ('UNKNOWN', r'.'),                            # Tout caractère non reconnu (erreur)
]

# Compilation des regex
token_regex = [(name, re.compile(pattern)) for name, pattern in TOKENS]

def tokenize(line):
    tokens = []
    while line:
        matched = False
        for token_name, token_re in token_regex:
            match = token_re.match(line)
            if match:
                if token_name != 'WHITESPACE':  # On ignore les espaces
                    tokens.append((token_name, match.group(0)))
                line = line[match.end():]  # Avance la position dans la ligne
                matched = True
                break
        if not matched:
            raise SyntaxError(f"Lexical error: unrecognized symbol {line[0]}")
    return tokens
