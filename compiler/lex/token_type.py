import re
from compiler.lex import token
from compiler.utils import cls_utils


class Operator(token.OperatorToken):
    """Represents a standard operator like + or *."""


class Plus(Operator):
    PATTERN = "+"
    PRECEDENCE = 13


class Minus(Operator):
    PATTERN = "-"
    PRECEDENCE = 13


class Times(Operator):
    PATTERN = "*"
    PRECEDENCE = 14


class Divide(Operator):
    PATTERN = "/"
    PRECEDENCE = 14


class LeftParens(token.LiteralToken):
    PATTERN = "("


class RightParens(token.LiteralToken):
    PATTERN = ")"


class Semicolon(token.LiteralToken):
    PATTERN = ";"


class Comma(token.LiteralToken):
    PATTERN = ","


class Assign(token.LiteralToken):
    PATTERN = "="


class LogicalOperator(token.LiteralToken):
    """Represents a logical operator like < or ==."""


class Equal(LogicalOperator):
    PATTERN = "=="


# Note LessThanOrEqualTo must come before LessThan
class LessThanOrEqualTo(LogicalOperator):
    PATTERN = "<="


class LessThan(LogicalOperator):
    PATTERN = "<"


# GreaterThanOrEqualTo must come before GreaterThan
class GreaterThanOrEqualTo(LogicalOperator):
    PATTERN = ">="


class GreaterThan(LogicalOperator):
    PATTERN = ">"


class Var(token.ReservedToken):
    PATTERN = "var"


class Const(token.ReservedToken):
    PATTERN = "const"


class For(token.ReservedToken):
    PATTERN = "for"


class While(token.ReservedToken):
    PATTERN = "while"


class If(token.ReservedToken):
    PATTERN = "if"


class Else(token.ReservedToken):
    PATTERN = "else"


class Float(token.Token[float]):
    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(r"[0-9]*\.[0-9]+", program) or re.match(
            r"[0-9]+\.[0-9]*", program
        )
        return match.group(0) if match else None

    # Set convert function to float constructor
    convert = float


class Integer(token.Token[int]):
    PATTERN = r"[0-9]+"
    # Set convert function to int constructor
    convert = int


class Id(token.StrToken):
    """Matches a user specified program identifier."""

    PATTERN = r"[_a-zA-Z]\w*"

    def __repr__(self) -> str:
        return "<ID>"


TOKENS: list[type[token.Token]] = [
    # Match reserved tokens before id
    *cls_utils.subclasses(token.ReservedToken),
    # 2 char operators must come before 1 char operators
    # e.g. == before =
    *cls_utils.subclasses(LogicalOperator),
    *cls_utils.subclasses(Operator),
    Assign,
    LeftParens,
    RightParens,
    Semicolon,
    Comma,
    Float,
    Integer,
    Id,
]
