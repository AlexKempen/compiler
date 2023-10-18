import unittest
from compiler.lex import lex, token_type


class TestLex(unittest.TestCase):
    def test_expression_tokens(self):
        test_case = " 5+ 34 * 2"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.Integer(5),
                token_type.Plus(),
                token_type.Integer(34),
                token_type.Times(),
                token_type.Integer(2),
            ],
        )

    def test_reserved_tokens(self):
        test_case = "for(), foreach"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.For(),
                token_type.LeftParens(),
                token_type.RightParens(),
                token_type.Comma(),
                token_type.Id("foreach"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
