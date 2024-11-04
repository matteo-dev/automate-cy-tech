#Tests pour l'analyseur lexical
from lexer import tokenize

if __name__ == "__main__":
    example_code = """
    cursor C1 at 100, 150
    set C1 color red
    move C1 by 50
    draw circle with C1 size 30
    rotate C1 by 90 degrees
    """
    
    lines = example_code.split('\n')
    for line in lines:
        tokens = tokenize(line)
        print(tokens)
