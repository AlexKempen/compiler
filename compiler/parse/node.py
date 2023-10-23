from __future__ import annotations
from abc import ABC

from compiler.lex import token
from compiler.parse import visitor


class Node(ABC):
    """Represents a node in an AST."""

    def accept(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor."""
        visitor.visit_node(self)

    # Not abstract since isn't strictly required
    @staticmethod
    def parse(tokens: token.TokenStream) -> Node:
        """Parses a stream of tokens into the given Node."""
        raise NotImplementedError()


class ParentNode(Node):
    def __init__(self, *children: Node) -> None:
        self.children = children
