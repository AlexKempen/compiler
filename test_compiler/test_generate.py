import unittest
from compiler.parse import parse
from compiler.generate import python_visitor, llvm
from compiler.lex import lex


class TestPythonVisitor(unittest.TestCase):
    def test_expression_parse(self):
        node = parse.parse_code("1 + 2 * 3; 2 * 3 + 1; 10 / 2;")
        visitor = python_visitor.PythonVisitor().visit(node)
        self.assertListEqual(visitor.results, [7, 7, 5])

    def test_node_count(self):
        node = parse.parse_code("2 * 3 + 1;")
        visitor = python_visitor.PythonVisitor().visit(node)
        self.assertEqual(visitor.node_count, 7)


class TestLlvm(unittest.TestCase):
    def test_call_parse(self):
        node = parse.parse_code("print(1 + 2 * 3); 2 * 2; print(2 * 3 + 1);")
        result = llvm.execute_node(node)
        results = [int(line) for line in result.splitlines()]
        self.assertListEqual(results, [7, 7])


if __name__ == "__main__":
    unittest.main()
