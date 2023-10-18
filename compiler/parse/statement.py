from __future__ import annotations

from compiler.lex import token, token_type

from compiler.parse import expression, node, visitor, parse_utils


class Statements(node.ParentNode):
    """Represents a block of one or more statements in a row."""

    def __init__(self, *statements: Statement) -> None:
        super().__init__(*statements)
        self.statements = statements

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statements(self)

    def __eq__(self, other: Statements) -> bool:
        return self.statements == other.statements

    @staticmethod
    def parse(tokens: token.TokenStream) -> Statements:
        """Recursively parses tokens into a list of statements.

        Currently terminates at eof.
        In the future, statements will also terminate at the end of a block (}).
        """
        statements = []
        while tokens:
            statements.append(Statement.parse(tokens))
        return Statements(*statements)


class Statement(node.Node):
    """Represents a statement, a construct spanning one or more complete lines."""

    @staticmethod
    def parse(tokens: token.TokenStream) -> Statement:
        if parse_utils.match(tokens, token_type.If):
            raise NotImplementedError()
        elif parse_utils.match(tokens, token_type.For):
            raise NotImplementedError()
        elif parse_utils.match(tokens, token_type.While):
            raise NotImplementedError()
        elif parse_utils.match(tokens, token_type.Var, token_type.Const):
            return Declaration.parse(tokens)
        elif parse_utils.match_sequence(tokens, token_type.Id, token_type.Assign):
            return Assignment.parse(tokens)
        elif parse_utils.match(tokens, token_type.Integer, token_type.Id):
            return ExprStatement.parse(tokens)
        parse_utils.unexpected_token(
            tokens.popleft(),
            token_type.If,
            token_type.For,
            token_type.While,
            token_type.Id,
            token_type.Integer,
        )


class ExprStatement(node.ParentNode, Statement):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    def __init__(self, expression: expression.Expression) -> None:
        super().__init__(expression)
        self.expression = expression

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expr_statement(self)

    def __eq__(self, other: ExprStatement) -> bool:
        return self.expression == other.expression

    @staticmethod
    def parse(tokens: token.TokenStream) -> ExprStatement:
        expr = expression.Expression.parse(tokens)
        parse_utils.expect(tokens, token_type.Semicolon)
        return ExprStatement(expr)


class Assignment(ExprStatement):
    """Represents an assignment of an expression to a variable."""

    def __init__(self, id: str, expression: expression.Expression) -> None:
        super().__init__(expression)
        self.id = id

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_assignment(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Assignment:
        id = parse_utils.expect(tokens, token_type.Id)
        parse_utils.expect(tokens, token_type.Assign)
        return Assignment(id.value, expression.Expression.parse(tokens))


class Declaration(Assignment):
    """Represents a variable declaration."""

    def __init__(self, id: str, expression: expression.Expression, const: bool) -> None:
        super().__init__(id, expression)
        self.const = const

    @staticmethod
    def parse(tokens: token.TokenStream) -> Declaration:
        if parse_utils.accept(tokens, token_type.Var):
            const = False
        elif parse_utils.accept(tokens, token_type.Const):
            const = True
        else:
            parse_utils.unexpected_token(
                tokens.popleft(), token_type.Var, token_type.Const
            )
        assignment = super().parse(tokens)
        return Declaration(assignment.id, assignment.expression, const)


class Control(node.ParentNode, Statement):
    """Represents a control structure like an if statement, function, or for loop."""

    def __init__(self, statements: Statements) -> None:
        super().__init__(statements)
        self.statements = statements


class For(Control):
    pass
