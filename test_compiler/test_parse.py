import unittest
from compiler.parsing import expression
from compiler.scanning import lex


class TestParse(unittest.TestCase):
    def test_normal_parse(self):
        node = expression.parse_expression(lex.lex("1 + 2 * 3"))
        self.assertEqual(node.evaluate(), 7)

    def test_order_parse(self):
        node = expression.parse_expression(lex.lex("2 * 3 + 1"))
        self.assertEqual(node.evaluate(), 7)


if __name__ == "__main__":
    unittest.main()
