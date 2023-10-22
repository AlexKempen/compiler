from __future__ import annotations
from abc import ABC
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from compiler.parse import node, expression, statement


class Visitor(ABC):
    """A class which can be used to visit each node in an AST.

    Note that the default implementations do not visit any nodes in the tree recursively.
    """

    def visit(self, node: node.Node) -> Self:
        """Invokes this visitor on the given node.

        Returns this Visitor.
        """
        node.accept(self)
        return self

    def visit_all(self, *nodes: node.Node) -> None:
        """Visits each node in nodes."""
        all(map(self.visit, nodes))

    def visit_children(self, node: node.ParentNode) -> Self:
        """Visits the children of the node."""
        self.visit_all(*node.children)
        return self

    def visit_node(self, node: node.Node) -> None:
        ...

    def visit_program(self, node: statement.Program) -> None:
        self.visit_children(node)

    def visit_block_statement(self, node: statement.BlockStatement) -> None:
        self.visit_children(node)

    def visit_statement(self, node: statement.Statement) -> None:
        ...

    def visit_expression_statement(self, node: statement.ExpressionStatement) -> None:
        self.visit_children(node)

    def visit_assignment(self, node: statement.Assignment) -> None:
        self.visit_children(node)

    def visit_expression(self, node: expression.Expression) -> None:
        ...

    def visit_call(self, node: expression.Call) -> None:
        self.visit_children(node)

    def visit_terminal_node(self, node: expression.TerminalNode) -> None:
        ...

    def visit_integer_node(self, node: expression.IntegerNode) -> None:
        ...

    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        self.visit_children(node)

    def visit_add(self, node: expression.Add) -> None:
        ...

    def visit_multiply(self, node: expression.Multiply) -> None:
        ...

    def visit_subtract(self, node: expression.Subtract) -> None:
        ...

    def visit_divide(self, node: expression.Divide) -> None:
        ...
