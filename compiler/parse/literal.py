from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar
from compiler.lex import token, token_type

from compiler.parse import parse_utils, visitor, expression


T = TypeVar("T")


@dataclass
class Literal(expression.Expression, Generic[T], ABC):
    """Represents a literal (i.e. constant or "hardcoded") value."""

    value: T

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_literal(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Literal:
        if parse_utils.match(tokens, token_type.True_, token_type.False_):
            return BooleanLiteral.parse(tokens)
        elif parse_utils.match(tokens, token_type.Integer):
            return IntegerLiteral.parse(tokens)
        parse_utils.unexpected_token(
            tokens, token_type.True_, token_type.False_, token_type.Integer
        )


@dataclass
class IntegerLiteral(Literal[int]):
    """Represents a node which corresponds to an integer literal."""

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_integer_literal(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> IntegerLiteral:
        tok = parse_utils.expect(tokens, token_type.Integer)
        return IntegerLiteral(tok.value)


@dataclass
class BooleanLiteral(Literal[bool]):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_boolean_literal(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> BooleanLiteral:
        if parse_utils.accept(tokens, token_type.True_):
            return BooleanLiteral(True)
        elif parse_utils.accept(tokens, token_type.False_):
            return BooleanLiteral(False)
        parse_utils.unexpected_token(tokens, token_type.True_, token_type.False_)
