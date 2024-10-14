#Tests pour l'analyseur syntaxique
import unittest
from parser import parse, SyntaxError

class TestParser(unittest.TestCase):

    def test_create_cursor_valid(self):
        tokens = [('KEYWORD', 'cursor'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'at'), ('NUMBER', '100'), ('NUMBER', '150')]
        self.assertTrue(parse(tokens))

    def test_create_cursor_invalid(self):
        tokens = [('KEYWORD', 'cursor'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'at'), ('NUMBER', '100')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

    def test_set_color_valid(self):
        tokens = [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'color'), ('COLOR', 'red')]
        self.assertTrue(parse(tokens))

    def test_set_color_invalid(self):
        tokens = [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'color'), ('NUMBER', '10')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

    def test_set_thickness_valid(self):
        tokens = [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'thickness'), ('NUMBER', '5')]
        self.assertTrue(parse(tokens))

    def test_set_thickness_invalid(self):
        tokens = [('KEYWORD', 'set'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'thickness')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

    def test_move_cursor_valid(self):
        tokens = [('KEYWORD', 'move'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '50')]
        self.assertTrue(parse(tokens))

    def test_move_cursor_invalid(self):
        tokens = [('KEYWORD', 'move'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

    def test_rotate_cursor_valid(self):
        tokens = [('KEYWORD', 'rotate'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'by'), ('NUMBER', '90'), ('KEYWORD', 'degrees')]
        self.assertTrue(parse(tokens))

    def test_draw_shape_valid(self):
        tokens = [('KEYWORD', 'draw'), ('SHAPE', 'circle'), ('KEYWORD', 'with'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'size'), ('NUMBER', '30')]
        self.assertTrue(parse(tokens))

    def test_draw_shape_invalid(self):
        tokens = [('KEYWORD', 'draw'), ('SHAPE', 'circle'), ('KEYWORD', 'with'), ('IDENTIFIER', 'C1'), ('KEYWORD', 'size')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

    def test_unknown_instruction(self):
        tokens = [('KEYWORD', 'unknown')]
        with self.assertRaises(SyntaxError):
            parse(tokens)

if __name__ == '__main__':
    unittest.main()
