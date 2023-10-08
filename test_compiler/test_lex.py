import unittest
from compiler.lex import lex, token_types


class TestLex(unittest.TestCase):
    def test_expression_tokens(self):
        test_case = " 5+ 34 * 2"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_types.Integer(5),
                token_types.Plus(),
                token_types.Integer(34),
                token_types.Times(),
                token_types.Integer(2),
            ],
        )

    def test_reserved_tokens(self):
        test_case = "for(), foreach"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_types.For(),
                token_types.LeftParens(),
                token_types.RightParens(),
                token_types.Comma(),
                token_types.Id("foreach"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
