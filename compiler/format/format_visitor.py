from compiler.format import setting
from compiler.parse import control, literal, node, statement, expression, visitor
from compiler.utils import str_utils


class FormatVisitor(visitor.Visitor):
    """Formats code."""

    def __init__(self, settings: setting.Settings) -> None:
        self.settings = settings
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
        self.program = "{\n" + self.visit_all(*node.body, tab=True)
        if self.settings.brace_style is setting.BraceStyle.COLLAPSE:
            self.program += "}"
        else:
            self.program += "}\n"

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

    def visit_literal(self, node: literal.Literal) -> None:
        self.program = str(node.value)

    def visit_binary_expression(self, node: expression.BinaryExpression) -> None:
        self.program = "{} {} {}".format(
            self.visit(node.left), node.operator, self.visit(node.right)
        )

    def get_body(
        self,
        body: statement.Statement | statement.BlockStatement,
        combine_with_next: bool = False,
    ) -> str:
        str_body = self.visit(body)
        if isinstance(body, statement.Statement):
            return "\n" + str_utils.tab(str_body)
        # If not collapse, body will already have trailing \n
        # If collapse, we need to add trailing \n unless we are combining with the next
        match self.settings.brace_style:
            case setting.BraceStyle.COLLAPSE:
                if combine_with_next:
                    return str_body
                return str_body + "\n"
            case setting.BraceStyle.EXPAND:
                return "\n" + str_body
            case setting.BraceStyle.END_EXPAND:
                return str_body

    def visit_for(self, node: control.For) -> None:
        self.program = "for ({} {} {}){}".format(
            self.visit(node.init),
            self.visit(node.test),
            self.visit(node.update),
            self.get_body(node.body),
        )

    def visit_if(self, node: control.If) -> None:
        if node.alternate:
            self.program = "if ({}){}{}".format(
                self.visit(node.test),
                self.get_body(node.consequent, True),
                self.visit(node.alternate),
            )
        else:
            self.program = "if ({}){}".format(
                self.visit(node.test), self.get_body(node.consequent)
            )

    def visit_else_if(self, node: control.ElseIf) -> None:
        if node.alternate:
            self.program = "else if ({}){}{}".format(
                self.visit(node.test),
                self.get_body(node.consequent, True),
                self.visit(node.alternate),
            )
        else:
            self.program = "else if ({}){}".format(
                self.visit(node.test), self.get_body(node.consequent)
            )

    def visit_else(self, node: control.Else) -> None:
        self.program = "else {}".format(self.visit(node.body))

        if self.settings.brace_style is setting.BraceStyle.COLLAPSE:
            self.program += "\n"
