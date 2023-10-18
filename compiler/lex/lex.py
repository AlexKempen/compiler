from collections import deque
from typing import Iterable
from compiler.lex import token, token_type


def lex(program: str) -> token.TokenStream:
    """Lexes the given program into a set of strings representing atomic tokens.

    Generally speaking, a token is a contiguous string which doesn't include any whitespace.
    """
    return deque(get_tokens(program))


def get_tokens(program: str) -> Iterable[token.Token]:
    while True:
        tok, program = token_type.extract_token(program)
        if tok:
            yield tok
        else:
            break
