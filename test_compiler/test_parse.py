import unittest
from compiler.parse import expression
from compiler.parse import parse, expression, statement


class TestParse(unittest.TestCase):
    def test_function_call_parse(self):
        node = parse.parse_code("myFunc(2, 3);")
        self.assertEqual(
            node,
            statement.Program(
                statement.ExpressionStatement(
                    expression.Call(
                        "myFunc",
                        expression.IntegerLiteral(2),
                        expression.IntegerLiteral(3),
                    )
                ),
            ),
        )

    def test_declaration_parse(self):
        node = parse.parse_code("const myVar = 2;")
        self.assertEqual(
            node,
            statement.Program(
                statement.VariableDeclaration(
                    "myVar", True, expression.IntegerLiteral(2)
                )
            ),
        )

    def test_regular_parse(self):
        node = parse.parse_code("1 + 2;")
        self.assertEqual(
            node,
            statement.Program(
                statement.ExpressionStatement(
                    expression.BinaryExpression(
                        expression.IntegerLiteral(1),
                        expression.IntegerLiteral(2),
                        "+",
                    )
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
