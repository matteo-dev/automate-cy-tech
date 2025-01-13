import re

# Définition des expressions régulières pour les différents types de tokens
TOKENS = [
    ('KEYWORD', r'\b(cursor|move|draw|set|if|else|for|while|color|thickness|size|animate|rotate|degrees|by|from|to)\b'),  # Mots-clés
    ('NUMBER', r'\b\d+\b'),  # Nombres
    ('COLOR', r'\b(red|blue|green|black)\b'),  # Couleurs prédéfinies
    ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z0-9_]*\b'),  # Identifiants pour les variables et les curseurs
    ('OPEN_BRACE', r'\{'),  # Opening brace
    ('CLOSE_BRACE', r'\}'),  # Closing brace
    ('SYMBOL', r'[=+*/<>():,;]'),  # Other symbols
    ('WHITESPACE', r'\s+'),  # Espaces et tabulations
    ('UNKNOWN', r'.'),  # Tout caractère non reconnu (pour gérer les erreurs)
]

# Compile the regex patterns
token_regex = [(name, re.compile(pattern)) for name, pattern in TOKENS]

# Fonction de tokenisation qui prend une ligne de code en entrée et retourne une liste de tokens
def tokenize(line):
    tokens = []  # List of recognized tokens
    while line:
        matched = False

        # Parcours des types de tokens pour trouver une correspondance
        for name, pattern in token_regex:
            match = pattern.match(line)
            if match:
                value = match.group(0)

                # Si ce n'est pas un espace, on ajoute le token à la liste
                if name != 'WHITESPACE':  # Ignore whitespace
                    tokens.append((name, value))

                # Avance la position dans la ligne pour continuer la recherche
                line = line[len(value):]
                matched = True
                break

         # Si aucun motif ne correspond, une erreur de syntaxe est levée
        if not matched:
            raise ValueError(f"Unexpected character in input: {line[0]}")
        
    return tokens
# Compilation des expressions régulières
token_regex = [(name, re.compile(pattern)) for name, pattern in TOKENS]


# Compile the regex patterns
compiled_tokens = [(name, re.compile(pattern)) for name, pattern in TOKENS]

# Example usage
if __name__ == "__main__":
    code = "for i from 0 to 5 { circle 50 }"
    token_list = tokenize(code)
    for token in token_list:
        print(token)
