import unittest
from parser import parse, SyntaxError

class TestParserWithStructures(unittest.TestCase):

    # Test pour une structure "if" valide
    def test_if_statement_valid(self):
        tokens = [
            ('KEYWORD', 'if'), ('CONDITION', 'condition'), ('SYMBOL', '{'),
            ('KEYWORD', 'move'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '50'),
            ('SYMBOL', '}')
        ]
        self.assertTrue(parse(tokens))

    # Test pour une boucle "for" valide
    def test_for_loop_valid(self):
        tokens = [
            ('KEYWORD', 'for'), ('IDENTIFIER', 'i'), ('KEYWORD', 'from'), ('NUMBER', '1'), ('KEYWORD', 'to'), ('NUMBER', '5'),
            ('SYMBOL', '{'), ('KEYWORD', 'draw'), ('SHAPE', 'circle'), ('KEYWORD', 'with'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'size'), ('NUMBER', '20'),
            ('SYMBOL', '}')
        ]
        self.assertTrue(parse(tokens))

    # Test pour une boucle "while" valide
    def test_while_loop_valid(self):
        tokens = [
            ('KEYWORD', 'while'), ('CONDITION', 'condition'), ('SYMBOL', '{'),
            ('KEYWORD', 'rotate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '15'), ('KEYWORD', 'degrees'),
            ('SYMBOL', '}')
        ]
        self.assertTrue(parse(tokens))

if __name__ == '__main__':
    unittest.main()
