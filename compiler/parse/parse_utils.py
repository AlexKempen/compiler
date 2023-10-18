from typing import NoReturn, TypeVar
from compiler.lex import token

T = TypeVar("T", bound=token.Token)


def assert_type(token: token.Token, token_type: type[T]) -> T:
    """Asserts the token is of the given token_type.

    throws:
        A ValueError if the next token does not match the given type.
    """
    if not isinstance(token, token_type):
        unexpected_token(token, token_type)
    return token


def expect(tokens: token.TokenStream, token_type: type[T]) -> T:
    """Asserts the next token is of the given token_type.

    throws:
        A ValueError if the next token does not match the given type.
    """
    token = tokens.popleft()
    return assert_type(token, token_type)


def accept(tokens: token.TokenStream, token_type: type[T]) -> T | None:
    """If the next token in tokens is of token_type, pops the token and returns it.Else, returns None."""
    return tokens.popleft() if match(tokens, token_type) else None  # type: ignore


def match(tokens: token.TokenStream, *token_types: type[token.Token]) -> bool:
    """Returns True if the next token matches any token in token_types."""
    return isinstance(tokens[0], token_types)


def match_sequence(tokens: token.TokenStream, *token_types: type[token.Token]) -> bool:
    """Returns True if the next sequence of tokens matches the sequence of token_types.

    In other words, the first token must match token_types[0], the second token token_types[1], etc.
    """
    for i, type in enumerate(token_types):
        if not isinstance(tokens[i], type):
            return False
    return True


def unexpected_token(actual: token.Token, *expected: type[token.Token]) -> NoReturn:
    """Throws an unexpected token parse error."""
    if len(expected) == 1:
        error_str = "Unexpected token - Expected token of type {}, got {}".format(
            repr(expected[0]), repr(actual)
        )
    else:
        error_str = "Unexpected token - Expected token of type [{}], got {}".format(
            ", ".join(map(repr, expected)), repr(actual)
        )
    raise ValueError(error_str)
