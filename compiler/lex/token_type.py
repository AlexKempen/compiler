from abc import ABC
import re
from compiler.lex import token
from compiler.utils import cls_utils


class MathOperator(token.OperatorToken, ABC):
    """Represents a standard operator like + or *."""


class Plus(MathOperator):
    PATTERN = "+"
    PRECEDENCE = 13


class Minus(MathOperator):
    PATTERN = "-"
    PRECEDENCE = 13


class Times(MathOperator):
    PATTERN = "*"
    PRECEDENCE = 14


class Divide(MathOperator):
    PATTERN = "/"
    PRECEDENCE = 14


class LeftParens(token.LiteralToken):
    PATTERN = "("


class RightParens(token.LiteralToken):
    PATTERN = ")"


class LeftBrace(token.LiteralToken):
    PATTERN = "{"


class RightBrace(token.LiteralToken):
    PATTERN = "}"


class Semicolon(token.LiteralToken):
    PATTERN = ";"


class Comma(token.LiteralToken):
    PATTERN = ","


class Assign(token.LiteralToken):
    PATTERN = "="


class LogicalOperator(token.OperatorToken):
    """Represents an operator like < or == which operates on or produces boolean expressions."""


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


class Var(token.StrReservedToken):
    PATTERN = "var"


class Const(token.StrReservedToken):
    PATTERN = "const"


class For(token.StrReservedToken):
    PATTERN = "for"


class While(token.StrReservedToken):
    PATTERN = "while"


class If(token.StrReservedToken):
    PATTERN = "if"


class Else(token.StrReservedToken):
    PATTERN = "else"


class Undefined(token.ReservedToken[None]):
    PATTERN = "undefined"

    @staticmethod
    def convert() -> None:
        return None


class True_(token.ReservedToken[bool]):
    PATTERN = "true"

    @staticmethod
    def convert() -> bool:
        return True


class False_(token.ReservedToken[bool]):
    PATTERN = "false"

    @staticmethod
    def convert() -> bool:
        return False


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


class Id(token.Token[str]):
    """Matches a user specified program identifier."""

    PATTERN = r"[_a-zA-Z]\w*"

    @staticmethod
    def convert(match: str) -> str:
        return match

    def __repr__(self) -> str:
        return "<ID>"


TOKENS: list[type[token.Token]] = [
    # Match reserved tokens before id
    *cls_utils.all_subclasses(token.ReservedToken),
    # 2 char operators must come before 1 char operators
    # e.g. == before =
    *cls_utils.subclasses(LogicalOperator),
    *cls_utils.subclasses(MathOperator),
    Assign,
    LeftParens,
    RightParens,
    LeftBrace,
    RightBrace,
    Semicolon,
    Comma,
    Float,
    Integer,
    Id,
]
