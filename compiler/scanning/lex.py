from typing import Iterator
from compiler.scanning import token, tokens


def lex(program: str) -> Iterator[token.Token]:
    """Lexes the given program into a set of strings representing atomic tokens.

    Generally speaking, a token is a contiguous string which doesn't include any whitespace.
    """
    while True:
        tok, program = tokens.extract_token(program)
        if tok:
            yield tok
        else:
            break
