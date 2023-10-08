"""A visitor which evalutes an AST Node using python."""
from compiler.parse import statement, visitor, node, expression


class PythonVisitor(visitor.Visitor):
    def __init__(self) -> None:
        self.node_count = 0
        self.results: list[int] = []

    def visit_node(self, _: node.Node) -> None:
        self.node_count += 1

    def visit_statement(self, node: statement.Statement) -> None:
        self.result = 0
        self.results.append(self.visit(node.expression).result)

    def visit_integer_node(self, node: expression.IntegerNode) -> None:
        self.result = node.value

    # # override binary operation to prevent default behavior
    def visit_binary_operation(self, node: expression.BinaryOperation) -> None:
        ...

    def visit_add(self, node: expression.Add) -> None:
        self.result = self.visit(node.left).result + self.visit(node.right).result

    def visit_subtract(self, node: expression.Subtract) -> None:
        self.result = self.visit(node.left).result - self.visit(node.right).result

    def visit_multiply(self, node: expression.Multiply) -> None:
        self.result = self.visit(node.left).result * self.visit(node.right).result

    def visit_divide(self, node: expression.Divide) -> None:
        self.result = self.visit(node.left).result // self.visit(node.right).result
