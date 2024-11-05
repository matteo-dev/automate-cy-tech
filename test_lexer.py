# Tests pour l'analyseur lexical
from lexer import tokenize

if __name__ == "__main__":
    # Exemple de code à analyser
    example_code = """
    cursor C1 at 100, 150
    set C1 color red
    move C1 by 50
    draw circle with C1 size 30
    rotate C1 by 90 degrees
    """
    
    # Séparation du code en lignes pour une analyse ligne par ligne
    lines = example_code.split('\n')
    for line in lines:
        if line.strip():  # Ignore les lignes vides
            tokens = tokenize(line)  # Appelle la fonction de tokenisation
            print(tokens)  # Affiche la liste des tokens reconnus pour chaque ligne
