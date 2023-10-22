from compiler.parse import node, statement, expression, visitor
from compiler.utils import str_utils


class FormatVisitor(visitor.Visitor):
    """Formats code."""

    def __init__(self) -> None:
        self.program = ""

    def visit(self, node: node.Node) -> str:
        super().visit(node)
        return self.program

    def visit_all(self, *nodes: node.Node, sep="", end="", tab=False) -> str:
        result = (sep + end).join(self.visit(node) for node in nodes) + end
        return str_utils.tab(result) if tab else result

    def visit_program(self, node: statement.Program) -> None:
        self.program = self.visit_all(*node.body)

    def visit_block_statement(self, node: statement.BlockStatement) -> None:
        self.program = self.visit_all(*node.body, tab=True)

    def visit_expression_statement(self, node: statement.ExpressionStatement) -> None:
        self.program = "{};\n".format(self.visit(node.expression))

    def visit_variable_declaration(self, node: statement.VariableDeclaration) -> None:
        prefix = "const" if node.const else "var"
        if node.initialization:
            self.program = "{} {} = {};\n".format(
                prefix, node.id, self.visit(node.initialization)
            )
        else:
            self.program = "{} {};\n".format(prefix, node.id)

    def visit_call(self, node: expression.Call) -> None:
        self.program = "{}({})".format(
            node.id, self.visit_all(*node.children, sep=", ")
        )

    def visit_literal(self, node: expression.IntegerLiteral) -> None:
        self.program = str(node.value)

    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        self.program = "{} {} {}".format(
            self.visit(node.left), node.operator, self.visit(node.right)
        )
