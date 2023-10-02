import unittest
from compiler.lex import lex, token_types


class TestLex(unittest.TestCase):
    def test_expression(self):
        test_case = " 5+ 34 */ "
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                token_types.Integer(5),
                token_types.Plus(),
                token_types.Integer(34),
                token_types.Times(),
                token_types.Divide(),
            ],
        )


if __name__ == "__main__":
    unittest.main()
