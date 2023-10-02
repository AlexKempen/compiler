"""A visitor which evalutes an AST Node using python."""
from compiler.parse import visitor, node


class PythonVisitor(visitor.Visitor):
    def __init__(self) -> None:
        self.node_count = 0
        self.result = 0

    def visit_node(self, _: node.Node) -> None:
        self.node_count += 1

    def visit_integer_node(self, node: node.IntegerNode) -> None:
        self.result = node.value

    def visit_add(self, node: node.Add) -> None:
        self.result = self.visit(node.left).result + self.visit(node.right).result

    def visit_subtract(self, node: node.Subtract) -> None:
        self.result = self.visit(node.left).result - self.visit(node.right).result

    def visit_multiply(self, node: node.Multiply) -> None:
        self.result = self.visit(node.left).result * self.visit(node.right).result

    def visit_divide(self, node: node.Divide) -> None:
        self.result = self.visit(node.left).result / self.visit(node.right).result
