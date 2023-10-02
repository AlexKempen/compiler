import unittest
from compiler.parse import expression
from compiler.lex import lex, token_types
from compiler.parse import parse, expression, statement


class TestParse(unittest.TestCase):
    def test_function_call_parse(self):
        node = parse.parse(lex.lex("myFunc(2, 3);"))
        self.assertEqual(
            node,
            statement.Statements(
                statement.Statement(
                    expression.Call(
                        token_types.Id("myFunc"),
                        expression.IntegerNode(2),
                        expression.IntegerNode(3),
                    )
                )
            ),
        )

    def test_regular_parse(self):
        node = parse.parse(lex.lex("1 + 2;"))
        self.assertEqual(
            node,
            statement.Statements(
                statement.Statement(
                    expression.Add(expression.IntegerNode(1), expression.IntegerNode(2))
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
