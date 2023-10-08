from __future__ import annotations
from abc import ABC

from collections import deque
from typing import Generic, TypeVar

from compiler.parse import node, visitor, parse_utils
from compiler.lex import token, token_types


class Expression(node.Node, ABC):
    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expression(self)


def get_precedence(tok: token.Token) -> int:
    return parse_utils.assert_token(tok, token.OperatorToken).PRECEDENCE


def parse_expression(
    tokens: deque[token.Token], previous_precedence: int = 0
) -> Expression:
    """Parses an expression."""
    if can_parse_call(tokens):
        left = parse_call(tokens)
    # handle id case
    else:
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

    def __init__(self, value: T) -> None:
        self.value = value

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_terminal_node(self)

    def __eq__(self, other: TerminalNode[T]) -> bool:
        return self.value == other.value


def make_terminal_node(tok: token.Token) -> TerminalNode:
    parse_utils.assert_token(tok, token.LiteralToken)
    return TerminalNode(tok.value)


class IntegerNode(TerminalNode[int], Expression):
    """Represents a node which corresponds to an integer literal."""

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_integer_node(self)


def make_integer_node(tok: token.Token) -> IntegerNode:
    parse_utils.assert_token(tok, token_types.Integer)
    return IntegerNode(tok.value)


class Call(Expression):
    """Represents a function call."""

    def __init__(self, id: token_types.Id, *arguments: Expression):
        self.id = id
        self.arguments = arguments

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        return visitor.visit_call(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit_all(*self.arguments)

    def __eq__(self, other: Call) -> bool:
        return self.id == other.id and self.arguments == other.arguments


def can_parse_call(tokens: deque[token.Token]) -> bool:
    return isinstance(tokens[0], token_types.Id) and isinstance(
        tokens[1], token_types.LeftParens
    )


def parse_call(tokens: deque[token.Token]) -> Call:
    id = parse_utils.assert_token(tokens.popleft(), token_types.Id)
    parse_utils.assert_token(tokens.popleft(), token_types.LeftParens)
    arguments = []
    while not isinstance(tokens[0], token_types.RightParens):
        arguments.append(parse_expression(tokens))
        if not parse_utils.try_next_token(tokens, token_types.Comma):
            break
    parse_utils.assert_token(tokens.popleft(), token_types.RightParens)
    return Call(id, *arguments)


class BinaryOperation(Expression, ABC):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_binary_operation(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit_all(self.left, self.right)

    def __eq__(self, other: BinaryOperation) -> bool:
        return self.left == other.left and self.right == other.right


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

    return constructor(left, right)


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
