"""A visitor which evalutes an AST Node using python."""
from compiler.parse import literal, statement, visitor, node, expression


class PythonVisitor(visitor.Visitor):
    def __init__(self) -> None:
        self.node_count = 0
        self.results: list[int] = []

    def visit(self, node: node.Node) -> int:
        super().visit(node)
        return self.result

    def visit_node(self, _: node.Node) -> None:
        self.node_count += 1

    def visit_expression_statement(self, node: statement.ExpressionStatement) -> None:
        self.result = 0
        self.results.append(self.visit(node.expression))

    def visit_integer_literal(self, node: literal.IntegerLiteral) -> None:
        self.result = node.value

    # # override binary operation to prevent default behavior
    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        lhs = self.visit(node.left)
        rhs = self.visit(node.right)
        match node.operator:
            case "+":
                self.result = lhs + rhs
            case "-":
                self.result = lhs - rhs
            case "*":
                self.result = lhs * rhs
            case "/":
                self.result = lhs // rhs
