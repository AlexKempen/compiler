from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from compiler.lex import token, token_types


class Node(ABC):
    """Represents a node in an AST."""


class Expression(Node, ABC):
    @abstractmethod
    def evaluate(self) -> int:
        """Evaluates an expression using Python."""
        ...


T = TypeVar("T")


class TerminalNode(Generic[T]):
    """Represents a terminal node in an AST.

    Typically corresponds to a token of some sort.
    """

    def __init__(self, type: str, value: T) -> None:
        self.type = type
        self.value = value


def make_terminal_node(tok: token.Token) -> TerminalNode:
    if isinstance(tok, token.LiteralToken):
        return TerminalNode(tok.type, tok.value)
    raise ValueError("Unexpected token - expected Literal, got: {}".format(tok))


class IntegerNode(TerminalNode[int], Expression):
    """Represents a node which corresponds to an integer literal."""

    def evaluate(self) -> int:
        return self.value


def make_integer_node(tok: token.Token) -> IntegerNode:
    if isinstance(tok, token_types.Integer):
        return IntegerNode(tok.type, tok.value)
    raise ValueError("Unexpected token - expected Integer, got: {}".format(tok))


class BinaryOperation(Expression, ABC):
    def __init__(self, left: Expression, right: Expression, op: TerminalNode[str]):
        self.left = left
        self.op = op
        self.right = right


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
    def evaluate(self) -> int:
        return self.left.evaluate() + self.right.evaluate()


class Multiply(BinaryOperation):
    def evaluate(self) -> int:
        return self.left.evaluate() * self.right.evaluate()


class Subtract(BinaryOperation):
    def evaluate(self) -> int:
        return self.left.evaluate() - self.right.evaluate()


class Divide(BinaryOperation):
    def evaluate(self) -> int:
        return self.left.evaluate() // self.right.evaluate()
