import unittest
from compiler.lex import lex, token_type


class TestLex(unittest.TestCase):
    def test_expression_token_lex(self):
        test_case = " 5+ 34 * 2"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.Integer(5),
                token_type.Plus(),
                token_type.Integer(34),
                token_type.Star(),
                token_type.Integer(2),
            ],
        )

    def test_reserved_token_lex(self):
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

    def test_assignment_lex(self):
        test_case = "== = 2 2.3"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.Equal(),
                token_type.Assign(),
                token_type.Integer(2),
                token_type.Float(2.3),
            ],
        )

    def test_logical_lex(self):
        test_case = "< <= > >="
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.LessThan(),
                token_type.LessThanOrEqualTo(),
                token_type.GreaterThan(),
                token_type.GreaterThanOrEqualTo(),
            ],
        )

    def test_declaration_lex(self):
        test_case = "const myVar = 2;"
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_type.Const(),
                token_type.Id("myVar"),
                token_type.Assign(),
                token_type.Integer(2),
                token_type.Semicolon(),
            ],
        )


if __name__ == "__main__":
    unittest.main()
