import unittest
from compiler.scanning import lex, tokens


class TestLexer(unittest.TestCase):
    def test_experssion(self):
        test_case = " 5+ 34 */ "
        result = lex.lex(test_case)
        self.assertListEqual(
            list(result),
            [
                tokens.Integer(5),
                tokens.Plus(),
                tokens.Integer(34),
                tokens.Times(),
                tokens.Divide(),
            ],
        )


if __name__ == "__main__":
    unittest.main()
