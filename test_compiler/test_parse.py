import unittest
from compiler.parse import expression
from compiler.scan import lex


class TestParse(unittest.TestCase):
    def test_normal_parse(self):
        node = expression.parse_expression(lex.lex("1 + 2 * 3"))
        self.assertEqual(node.evaluate(), 7)

    def test_order_parse(self):
        node = expression.parse_expression(lex.lex("2 * 3 + 1"))
        self.assertEqual(node.evaluate(), 7)


if __name__ == "__main__":
    unittest.main()
