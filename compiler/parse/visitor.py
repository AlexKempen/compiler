from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from compiler.parse import node


class Visitor(ABC):
    """A class which can be used to visit each node in an AST.

    Note that the default implementations do not visit any nodes in the tree recursively.
    """

    def visit(self, node: node.Node) -> Self:
        """Invokes this visitor on the given node."""
        node.accept(self)
        return self

    def visit_node(self, node: node.Node) -> None:
        ...

    def visit_expression(self, node: node.Expression) -> None:
        ...

    def visit_terminal_node(self, node: node.TerminalNode) -> None:
        ...

    def visit_integer_node(self, node: node.IntegerNode) -> None:
        ...

    def visit_binary_operation(self, node: node.BinaryOperation) -> None:
        ...

    def visit_add(self, node: node.Add) -> None:
        ...

    def visit_multiply(self, node: node.Multiply) -> None:
        ...

    def visit_subtract(self, node: node.Subtract) -> None:
        ...

    def visit_divide(self, node: node.Divide) -> None:
        ...
