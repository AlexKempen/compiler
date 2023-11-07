from abc import ABC
import re
from compiler.lex import token
from compiler.utils import cls_utils


class Operator(token.OperatorToken, ABC):
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


class Equal(Operator):
    PATTERN = "=="
    PRECEDENCE = 999


# Note LessThanOrEqualTo must come before LessThan
class LessThanOrEqualTo(Operator):
    PATTERN = "<="
    PRECEDENCE = 999


class LessThan(Operator):
    PATTERN = "<"
    PRECEDENCE = 999


# GreaterThanOrEqualTo must come before GreaterThan
class GreaterThanOrEqualTo(Operator):
    PATTERN = ">="
    PRECEDENCE = 999


class GreaterThan(Operator):
    PATTERN = ">"
    PRECEDENCE = 999


class LogicalOperator(token.OperatorToken):
    """Represents an operator like < or == which operates on or produces boolean expressions."""


class And(LogicalOperator):
    PATTERN = "&&"


class Or(LogicalOperator):
    PATTERN = "||"


class Not(LogicalOperator):
    PATTERN = "!"


class SyntaxToken(token.PatternToken, ABC):
    """Represents a syntax token like "(" or "}"."""


class LeftParens(SyntaxToken):
    PATTERN = "("


class RightParens(SyntaxToken):
    PATTERN = ")"


class LeftBrace(SyntaxToken):
    PATTERN = "{"


class RightBrace(SyntaxToken):
    PATTERN = "}"


class Semicolon(SyntaxToken):
    PATTERN = ";"


class Comma(SyntaxToken):
    PATTERN = ","


class Assign(SyntaxToken):
    """Keep assign as a special form of syntax since FS doesn't allow assignment as an expression."""

    PATTERN = "="


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


class Undefined(token.Token[None]):
    @classmethod
    def match(cls, program: str) -> str | None:
        return token.reserved_match(program, "undefined")

    @staticmethod
    def convert() -> None:
        return None


class Boolean(token.Token[bool]):
    @classmethod
    def match(cls, program: str) -> str | None:
        return token.reserved_match(program, "true|false")

    @staticmethod
    def convert(match: str) -> bool:
        return True if match == "true" else False


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
    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(r"[0-9]+", program)
        return match.group(0) if match else None

    # Set convert function to int constructor
    convert = int


class Id(token.Token[str]):
    """Matches a user specified program identifier."""

    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(r"[_a-zA-Z]\w*", program)
        return match.group(0) if match else None

    @staticmethod
    def convert(match: str) -> str:
        return match


TOKENS: list[type[token.Token]] = [
    # Match reserved tokens before id
    *cls_utils.all_subclasses(token.ReservedToken),
    # 2 char operators must come before 1 char operators
    # e.g. == before =
    *cls_utils.subclasses(LogicalOperator),
    *cls_utils.subclasses(Operator),
    *cls_utils.subclasses(SyntaxToken),
    Undefined,
    Boolean,
    Float,
    Integer,
    Id,
]
