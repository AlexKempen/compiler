from typing import NoReturn, TypeVar, overload
from functools import singledispatch
from compiler.lex import token

T = TypeVar("T", bound=token.Token)


def expect(tokens: token.TokenStream, token_type: type[T]) -> T:
    """Asserts the next token is of the given token_type and consumes it.

    throws:
        A ValueError if the next token does not match the given type.
    """
    if tok := match(tokens, token_type):
        # Token always matches
        tokens.popleft()
        return tok
    unexpected_token(tokens, token_type)


def expect_sequence(tokens: token.TokenStream, *token_types: type[T]) -> None:
    for token_type in token_types:
        expect(tokens, token_type)


def accept(tokens: token.TokenStream, token_type: type[T]) -> T | None:
    """If the next token in tokens is of token_type, pops the token and returns it. Else, returns None."""
    if next := match(tokens, token_type):
        tokens.popleft()
    return next


def match(tokens: token.TokenStream, *token_types: type[T]) -> T | None:
    """If the next token matches any token in token_types, returns it. Else, returns None.

    No tokens are consumed from the stream."""
    if len(tokens) >= 1 and isinstance(tokens[0], token_types):
        return tokens[0]


def match_sequence(tokens: token.TokenStream, *token_types: type[token.Token]) -> bool:
    """Returns True if the next sequence of tokens matches the sequence of token_types.

    In other words, the first token must match token_types[0], the second token token_types[1], etc.

    No tokens are consumed from the stream."""
    if len(tokens) < len(token_types):
        return False
    for i, type in enumerate(token_types):
        if not isinstance(tokens[i], type):
            return False
    return True


def expected_token_type(*expected: type[token.Token]) -> str:
    """Returns a message of the form: 'Expected token of type ...'"""
    if len(expected) == 1:
        return "Expected token of type {}".format(expected[0].type())
    return "Expected token of type [{}]".format(
        ", ".join(map(lambda ex: ex.type(), expected))
    )


def invalid_token(tok: token.Token, *expected: type[token.Token]) -> NoReturn:
    """Throws an unexpected token parse error."""
    expected_str = expected_token_type(*expected)
    error_str = "Unexpected token - {}, got {}".format(expected_str, tok.type())
    raise ValueError(error_str)


def unexpected_token(
    tokens: token.TokenStream, *expected: type[token.Token]
) -> NoReturn:
    """Throws an unexpected token parse error.

    Also handles the case where tokens is exhausted.
    """
    expected_str = expected_token_type(*expected)
    if not tokens:
        error_str = "Unexpected end of input - {}".format(expected_str)
        raise ValueError(error_str)
    invalid_token(tokens[0], *expected)
