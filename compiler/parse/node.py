from __future__ import annotations
from abc import ABC

from compiler.parse import visitor


class Node(ABC):
    """Represents a node in an AST."""

    def accept(self, visitor: visitor.Visitor) -> None:
        visitor.visit_node(self)