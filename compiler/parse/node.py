from __future__ import annotations
from abc import ABC

from compiler.parse import visitor


class Node(ABC):
    """Represents a node in an AST."""

    def accept(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor, executing the appropriate method."""
        visitor.visit_node(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor for the children of the node."""
        ...
