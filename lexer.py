import re

# Définition des expressions régulières pour les différents types de tokens
TOKENS = [
    ('KEYWORD', r'\b(cursor|move|draw|set|if|else|for|while|color|thickness|size|animate|rotate|degrees|by)\b'),  # Mots-clés
    ('NUMBER', r'\b\d+\b'),  # Nombres
    ('COLOR', r'\b(red|blue|green|black)\b'),  # Couleurs prédéfinies
    ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),  # Identifiants pour les variables et les curseurs
    ('SYMBOL', r'[=+*/<>(){}:,]'),  # Symboles divers (opérateurs, parenthèses, etc.)
    ('WHITESPACE', r'\s+'),  # Espaces et tabulations
    ('UNKNOWN', r'.'),  # Tout caractère non reconnu (pour gérer les erreurs)
]

# Compilation des expressions régulières
token_regex = [(name, re.compile(pattern)) for name, pattern in TOKENS]

# Fonction de tokenisation qui prend une ligne de code en entrée et retourne une liste de tokens
def tokenize(line):
    tokens = []  # Liste des tokens reconnus
    while line:
        matched = False  # Indicateur de correspondance

        # Parcours des types de tokens pour trouver une correspondance
        for token_name, token_re in token_regex:
            match = token_re.match(line)  # Recherche au début de la ligne
            if match:
                # Si ce n'est pas un espace, on ajoute le token à la liste
                if token_name != 'WHITESPACE':
                    tokens.append((token_name, match.group(0)))
                
                # Avance la position dans la ligne pour continuer la recherche
                line = line[match.end():]
                matched = True
                break

        # Si aucun motif ne correspond, une erreur de syntaxe est levée
        if not matched:
            raise SyntaxError(f"Lexical error: unrecognized symbol {line[0]}")
    
    return tokens  # Retourne la liste des tokens
