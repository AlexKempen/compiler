import unittest
from compiler.parse import expression
from compiler.generate import python_visitor
from compiler.lex import lex


class TestParse(unittest.TestCase):
    def test_normal_parse(self):
        node = expression.parse_expression(lex.lex("1 + 2 * 3;"))
        result = python_visitor.PythonVisitor().visit(node).result
        self.assertEqual(result, 7)

    def test_order_parse(self):
        node = expression.parse_expression(lex.lex("2 * 3 + 1;"))
        result = python_visitor.PythonVisitor().visit(node).result
        self.assertEqual(result, 7)

    def test_node_count(self):
        node = expression.parse_expression(lex.lex("2 * 3 + 1;"))
        visitor = python_visitor.PythonVisitor().visit(node)
        self.assertEqual(visitor.node_count, 5)


if __name__ == "__main__":
    unittest.main()
