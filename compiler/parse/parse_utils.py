from collections import deque
from typing import Type, TypeVar
from compiler.lex import token

T = TypeVar("T", bound=token.Token)


def assert_token(tok: token.Token, token_type: Type[T]) -> T:
    """Asserts the token is of the given token_type.

    throws:
        A ValueError if the next token does not match the given type.
    """
    if not isinstance(tok, token_type):
        raise ValueError(
            "Unexpected token - Expected token of type {}, got {}".format(
                token_type.__name__, tok.type
            )
        )
    return tok


def try_next_token(tokens: deque[token.Token], token_type: Type[T]) -> T | None:
    """If the next token in tokens is of token_type, pops the token and returns it. Else, returns None."""
    token = tokens[0]
    if isinstance(token, token_type):
        # Make type checker happy
        tokens.popleft()
        return token
    return None
