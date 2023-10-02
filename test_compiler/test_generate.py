import unittest
from compiler.parse import parse
from compiler.generate import python_visitor
from compiler.lex import lex


class TestGenerate(unittest.TestCase):
    def test_normal_parse(self):
        node = parse.parse(lex.lex("1 + 2 * 3; 1 * 3;"))
        visitor = python_visitor.PythonVisitor().visit(node)
        self.assertEqual(visitor.results, [7, 3])


if __name__ == "__main__":
    unittest.main()
