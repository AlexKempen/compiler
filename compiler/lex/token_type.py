import re
from compiler.lex import token
from compiler.utils import cls_utils


def extract_token(program: str) -> tuple[token.Token | None, str]:
    """Extracts the next token from program.

    Returns a tuple containing the token that was extracted (or None) and the program with the token removed.
    """
    program = skip_whitespace(program)
    for token_type in TOKENS:
        match = token_type.match(program)
        if match:
            program = program.removeprefix(match)
            return (make_token(token_type, match), program)
    return (None, program)


def make_token(token_type: type[token.Token], match: str) -> token.Token:
    """Constructs a token of token_type from match if necessary."""
    if issubclass(token_type, token.LiteralToken):
        return token_type()
    else:
        return token_type(token_type.convert(match))


def skip_whitespace(program: str) -> str:
    """Skips to the next non-whitespace character."""
    while program and program[0] in " \t\n":
        program = program[1:]
    return program


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


class LessThan(LogicalOperator):
    PATTERN = "<"


class LessThanOrEqualTo(LogicalOperator):
    PATTERN = "<="


class GreaterThan(LogicalOperator):
    PATTERN = ">"


class GreaterThanOrEqualTo(LogicalOperator):
    PATTERN = ">="


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
        return "Identifier"


TOKENS = [
    # Match reserved tokens before id
    *cls_utils.subclasses(token.ReservedToken),
    # 2 char operators must come before 1 char operators
    # e.g. == before =
    *cls_utils.subclasses(LogicalOperator),
    *cls_utils.subclasses(Operator),
    LeftParens,
    RightParens,
    Semicolon,
    Comma,
    Float,
    Integer,
    Id,
]
