from typing import NoReturn, Type, TypeGuard, TypeVar
from compiler.lex import token

T = TypeVar("T", bound=token.Token)


def assert_type(token: token.Token, token_type: Type[T]) -> T:
    """Asserts the token is of the given token_type.

    throws:
        A ValueError if the next token does not match the given type.
    """
    if not isinstance(token, token_type):
        unexpected_token(token, token_type)
    return token


def expect(tokens: token.TokenStream, token_type: Type[T]) -> T:
    """Asserts the next token is of the given token_type.

    throws:
        A ValueError if the next token does not match the given type.
    """
    token = tokens.popleft()
    return assert_type(token, token_type)


def accept(tokens: token.TokenStream, token_type: Type[T]) -> T | None:
    """If the next token in tokens is of token_type, pops the token and returns it.Else, returns None."""
    return tokens.popleft() if match_sequence(tokens, token_type) else None  # type: ignore


def match_any(tokens: token.TokenStream, *token_types: Type[token.Token]) -> bool:
    return isinstance(tokens[0], token_types)


def match_sequence(tokens: token.TokenStream, *token_types: Type[token.Token]) -> bool:
    """Returns True if the next set of tokens match token_types.

    Note this is a 1-to-1 matching, meaning the first token must match
    token_types[0], the second token token_types[1], etc.
    """
    for i, type in enumerate(token_types):
        if not isinstance(tokens[i], type):
            return False
    return True


def unexpected_token(actual: token.Token, *expected: Type[token.Token]) -> NoReturn:
    """Throws an unexpected token parse error."""
    if len(expected) == 1:
        error_str = "Unexpected token - Expected token of type {}, got {}".format(
            token.token_type(expected[0]), actual.type
        )
    else:
        error_str = "Unexpected token - Expected token of type [{}], got {}".format(
            ", ".join(map(token.token_type, expected)), actual.type
        )
    raise ValueError(error_str)
