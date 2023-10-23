from collections import deque
from typing import Iterable
from compiler.lex import token
from compiler.lex import token_type


def lex(program: str) -> token.TokenStream:
    """Lexes the given program into a set of strings representing atomic tokens.

    Generally speaking, a token is a contiguous string which doesn't include any whitespace.
    """
    return deque(get_tokens(program))


def extract_token(program: str) -> tuple[token.Token | None, str]:
    """Extracts the next token from program.

    Returns a tuple containing the token that was extracted (or None) and the program with the token removed.
    """
    program = skip_whitespace(program)
    for tok_type in token_type.TOKENS:
        match = tok_type.match(program)
        if match:
            program = program.removeprefix(match)
            return (make_token(tok_type, match), program)
    return (None, program)


def make_token(token_type: type[token.Token], match: str) -> token.Token:
    """Constructs a token of token_type from match if necessary."""
    if isinstance(token_type, token.LiteralToken):
        return token_type()
    return token_type(token_type.convert(match))


def skip_whitespace(program: str) -> str:
    """Skips to the next non-whitespace character."""
    while program and program[0] in " \t\n":
        program = program[1:]
    return program


def get_tokens(program: str) -> Iterable[token.Token]:
    while True:
        tok, program = extract_token(program)
        if tok:
            yield tok
        else:
            break
