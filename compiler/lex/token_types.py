import re
from compiler.lex import token


def extract_token(program: str) -> tuple[token.Token | None, str]:
    """Extracts the next token from program.

    Returns a tuple containing the token that was extracted (or None) and the program with the token removed.
    """
    program = skip_whitespace(program)
    for token_type in TOKENS:
        match = token_type.match(program)
        if match:
            program = program.removeprefix(match)
            return (token.make_token(token_type, match), program)
    return (None, program)


def skip_whitespace(program: str) -> str:
    """Skips to the next non-whitespace character."""
    while program and program[0] in " \t\n":
        program = program[1:]
    return program


class Plus(token.OperatorToken):
    PATTERN = "+"
    PRECEDENCE = 13


class Minus(token.OperatorToken):
    PATTERN = "-"
    PRECEDENCE = 13


class Times(token.OperatorToken):
    PATTERN = "*"
    PRECEDENCE = 14


class Divide(token.OperatorToken):
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


class Integer(token.Token[int]):
    PATTERN = r"[0-9]+"
    # Set convert function to int constructor
    convert = int


class Id(token.StrToken):
    """Matches a user specified program identifier."""

    PATTERN = r"[_a-zA-Z]\w*"

    # @classmethod
    # def match(cls, program: str) -> str | None:
    #     # Don't match literal tokens
    #     # if any(map(lambda type: type.match(program), LITERAL_TOKENS)):
    #     #     return None
    #     return super().match(program)


class Float(token.Token[float]):
    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(r"[0-9]*\.[0-9]+", program) or re.match(
            r"[0-9]+\.[0-9]*", program
        )
        return match.group(0) if match else None

    # Set convert function to float constructor
    convert = float


class For(token.ReservedToken):
    PATTERN = "for"


class While(token.ReservedToken):
    PATTERN = "while"


class If(token.ReservedToken):
    PATTERN = "if"


RESERVED_TOKENS = [If, For, While]

# Longer matches should come first
TOKENS = [
    Plus,
    Minus,
    Times,
    Divide,
    LeftParens,
    RightParens,
    Semicolon,
    Comma,
    Float,
    Integer,
    *RESERVED_TOKENS,
    Id,
]
