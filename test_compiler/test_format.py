import unittest
from compiler.format import formatter

FORMATTED = """1 + 3;
print(3 * 2);
print(2 + 2);
var myVar;
const val = 4;
"""
UGLY = """1+  3;

print  
(3*2 ) ;

print(2+2);
var myVar ;
const   val=4;
"""


class TestFormat(unittest.TestCase):
    def test_expression_parse(self):
        result = formatter.format(UGLY)
        self.assertEqual(result, FORMATTED)


if __name__ == "__main__":
    unittest.main()
