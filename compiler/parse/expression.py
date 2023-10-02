from __future__ import annotations
from abc import ABC

from collections import deque
from typing import Generic, TypeVar

from compiler.parse import node, visitor
from compiler.lex import token, token_types


class Expression(node.Node, ABC):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expression(self)


def parse_expression(
    tokens: deque[token.Token], previous_precedence: int = 0
) -> Expression:
    left = make_integer_node(tokens.popleft())

    while (
        isinstance(tokens[0], token.OperatorToken)
        and get_precedence(tokens[0]) > previous_precedence
    ):
        op_token = tokens.popleft()
        right = parse_expression(tokens, get_precedence(op_token))
        left = make_binary_operation(left, right, op_token)

    return left


T = TypeVar("T")


class TerminalNode(node.Node, Generic[T]):
    """Represents a terminal node in an AST.

    Typically corresponds to a token of some sort.
    """

    def __init__(self, type: str, value: T) -> None:
        self.type = type
        self.value = value

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_terminal_node(self)


def make_terminal_node(tok: token.Token) -> TerminalNode:
    if isinstance(tok, token.LiteralToken):
        return TerminalNode(tok.type, tok.value)
    raise ValueError("Unexpected token - expected Literal, got: {}".format(tok))


class IntegerNode(TerminalNode[int], Expression):
    """Represents a node which corresponds to an integer literal."""

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_integer_node(self)


def make_integer_node(tok: token.Token) -> IntegerNode:
    if isinstance(tok, token_types.Integer):
        return IntegerNode(tok.type, tok.value)
    raise ValueError("Unexpected token - expected Integer, got: {}".format(tok))


def get_precedence(tok: token.Token) -> int:
    if not isinstance(tok, token.OperatorToken):
        raise SyntaxError("Expected operator, got: {}".format(tok))
    return tok.PRECEDENCE


class BinaryOperation(Expression, ABC):
    def __init__(self, left: Expression, right: Expression, op: TerminalNode[str]):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_binary_operation(self)


def make_binary_operation(
    left: Expression, right: Expression, tok: token.Token
) -> BinaryOperation:
    if isinstance(tok, token_types.Plus):
        constructor = Add
    elif isinstance(tok, token_types.Minus):
        constructor = Subtract
    elif isinstance(tok, token_types.Times):
        constructor = Multiply
    elif isinstance(tok, token_types.Divide):
        constructor = Divide
    else:
        raise ValueError("Unexpected token - expected Operator, got: {}".format(token))

    return constructor(left, right, make_terminal_node(tok))


class Add(BinaryOperation):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_add(self)


class Multiply(BinaryOperation):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_multiply(self)


class Subtract(BinaryOperation):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_subtract(self)


class Divide(BinaryOperation):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_divide(self)
