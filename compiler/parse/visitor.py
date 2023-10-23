from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from compiler.parse import node, expression, statement, control, literal


class Visitor(ABC):
    """A class which can be used to visit each node in an AST.

    Note that the default implementations do not visit any nodes in the tree recursively.
    """

    def execute(self, node: node.Node) -> Self:
        """Invokes this visitor on the given node."""
        self.visit(node)
        return self

    def visit(self, node: node.Node) -> Self:
        """Invokes this visitor on the given node.

        Returns the result passed to __init__.
        """
        node.accept(self)
        return self

    def visit_all(self, *nodes: node.Node) -> Self:
        """Visits each node in nodes."""
        all(map(self.visit, nodes))
        return self

    def visit_children(self, node: node.ParentNode) -> Self:
        """Visits all the child nodes of a given node in arbitrary order."""
        return self.visit_all(*node.children)

    def visit_node(self, node: node.Node) -> None:
        ...

    def visit_program(self, node: statement.Program) -> None:
        self.visit_children(node)

    def visit_block_statement(self, node: statement.BlockStatement) -> None:
        self.visit_children(node)

    def visit_expression_statement(self, node: statement.ExpressionStatement) -> None:
        self.visit_children(node)

    def visit_variable_declaration(self, node: statement.VariableDeclaration) -> None:
        self.visit_children(node)

    def visit_assignment(self, node: statement.Assignment) -> None:
        self.visit_children(node)

    def visit_call(self, node: expression.Call) -> None:
        self.visit_children(node)

    def visit_literal(self, node: literal.Literal) -> None:
        ...

    def visit_integer_literal(self, node: literal.IntegerLiteral) -> None:
        ...

    def visit_boolean_literal(self, node: literal.BooleanLiteral) -> None:
        ...

    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        self.visit_children(node)

    def visit_logical_expression(self, node: expression.LogicalExpression) -> None:
        self.visit_children(node)

    def visit_for(self, node: control.For) -> None:
        self.visit_children(node)

    def visit_while(self, node: control.While) -> None:
        self.visit_children(node)

    def visit_if(self, node: control.If) -> None:
        self.visit_children(node)

    def visit_else_if(self, node: control.ElseIf) -> None:
        self.visit_children(node)

    def visit_else(self, node: control.Else) -> None:
        self.visit_children(node)
