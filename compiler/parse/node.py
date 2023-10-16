from __future__ import annotations
from abc import ABC
from compiler.lex import token

from compiler.parse import visitor


class Node(ABC):
    """Represents a node in an AST."""

    def accept(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor, executing the appropriate method."""
        visitor.visit_node(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor for the children of the node."""
        ...

    @staticmethod
    def parse(tokens: token.TokenStream) -> Node:
        """Parses a stream of tokens into the given Node."""
        raise NotImplementedError()
