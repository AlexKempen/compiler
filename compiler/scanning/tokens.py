import re
from compiler.scanning import token


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


class Plus(token.LiteralToken):
    PATTERN = "+"


class Minus(token.LiteralToken):
    PATTERN = "-"


class Times(token.LiteralToken):
    PATTERN = "*"


class Divide(token.LiteralToken):
    PATTERN = "/"


class LeftParens(token.LiteralToken):
    PATTERN = "("


class RightParens(token.LiteralToken):
    PATTERN = ")"


class Integer(token.Token[int]):
    PATTERN = r"[0-9]+"
    # Set convert function to int constructor
    convert = int


class Id(token.StrToken):
    """Matches a user specified program identifier.

    TODO: Don't match reserved keywords like `for` and `if`
    """

    PATTERN = r"[_a-zA-Z]\w*"


class Float(token.Token[float]):
    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(r"[0-9]*\.[0-9]+", program) or re.match(
            r"[0-9]+\.[0-9]*", program
        )
        return match.group(0) if match else None

    # Set convert function to float constructor
    convert = float


# Longer matches should come first
TOKENS: list[type[token.Token]] = [
    Float,
    Integer,
    Plus,
    Minus,
    Times,
    Divide,
    LeftParens,
    RightParens,
    Id,
]
