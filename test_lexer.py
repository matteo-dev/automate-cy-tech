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
        
# Test cases
drawpp_code = [
    "for i from 0 to 5 { drawCircle(); }",  # Simple for loop
    "while x < 10 { move(10, 0); }",        # Simple while loop
    "if condition { drawSquare(); } else { drawCircle(); }",  # Mixed test
]

for code in drawpp_code:
    print(f"Testing code: {code}")
    try:
        tokens = tokenize(code)
        for token in tokens:
            print(token)
    except ValueError as e:
        print(f"Error: {e}")
    print("-" * 40)
