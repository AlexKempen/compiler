from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from typing import Generic, TypeVar

from compiler.parse import node, visitor, parse_utils
from compiler.lex import token, token_type


class Expression(node.Node, ABC):
    """Represents an arithmetic or logical expression."""

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expression(self)

    @staticmethod
    def parse(tokens: token.TokenStream, previous_precedence: int = 0) -> Expression:
        """Parses an expression."""
        if parse_utils.match_sequence(tokens, token_type.Id, token_type.LeftParens):
            left = Call.parse(tokens)
        # handle id case
        elif parse_utils.match(tokens, token_type.Integer):
            left = IntegerNode.parse(tokens)
        else:
            parse_utils.unexpected_token(tokens, token_type.Id, token_type.Integer)

        while (
            tok := parse_utils.match(tokens, token.OperatorToken)
        ) and tok.PRECEDENCE > previous_precedence:
            tokens.popleft()  # Pop operator token
            right = Expression.parse(tokens, tok.PRECEDENCE)
            left = make_binary_expression(left, right, tok)

        return left


T = TypeVar("T")


@dataclass
class TerminalNode(node.Node, Generic[T]):
    """Represents a terminal node in an AST.

    Typically corresponds to a token of some sort.
    """

    value: T

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_terminal_node(self)

    # def parse(self, tokens: token.TokenStream) -> Self:
    #     tok = parse_utils.expect(tokens, token.LiteralToken)
    #     return TerminalNode(tok.value)


class IntegerNode(TerminalNode[int], Expression):
    """Represents a node which corresponds to an integer literal."""

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_integer_node(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> IntegerNode:
        tok = parse_utils.expect(tokens, token_type.Integer)
        return IntegerNode(tok.value)


@dataclass
class Call(node.ParentNode, Expression):
    """Represents a function call."""

    def __init__(self, id: str, *arguments: Expression):
        super().__init__(*arguments)
        self.id = id
        self.arguments = arguments

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        return visitor.visit_call(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Call:
        id = parse_utils.expect(tokens, token_type.Id).value
        parse_utils.expect(tokens, token_type.LeftParens)
        arguments = []
        while not parse_utils.match(tokens, token_type.RightParens):
            arguments.append(Expression.parse(tokens))
            if not parse_utils.accept(tokens, token_type.Comma):
                break
        parse_utils.expect(tokens, token_type.RightParens)
        return Call(id, *arguments)


@dataclass
class BinaryExpression(node.ParentNode, Expression, ABC):
    """Represents an operation with two operands."""

    left: Expression
    right: Expression

    def __post_init__(self):
        super().__init__(self.left, self.right)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_binary_expression(self)


def make_binary_expression(
    left: Expression, right: Expression, tok: token.Token
) -> BinaryExpression:
    if isinstance(tok, token_type.Plus):
        constructor = Add
    elif isinstance(tok, token_type.Minus):
        constructor = Subtract
    elif isinstance(tok, token_type.Times):
        constructor = Multiply
    elif isinstance(tok, token_type.Divide):
        constructor = Divide
    else:
        parse_utils.invalid_token(
            tok,
            token_type.Plus,
            token_type.Minus,
            token_type.Times,
            token_type.Divide,
        )

    return constructor(left, right)


@dataclass
class Add(BinaryExpression):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_add(self)


@dataclass
class Multiply(BinaryExpression):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_multiply(self)


@dataclass
class Subtract(BinaryExpression):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_subtract(self)


@dataclass
class Divide(BinaryExpression):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_divide(self)


class LogicalExpression(BinaryExpression):
    """An operation which evaluates to True or False."""

    pass
