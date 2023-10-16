from __future__ import annotations

from compiler.lex import token, token_types

from compiler.parse import expression, node, visitor, parse_utils


class Statements(node.Node):
    """Represents a block of one or more statements in a row."""

    def __init__(self, *statements: Statement) -> None:
        self.statements = statements

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statements(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit_all(*self.statements)

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
        if parse_utils.match_sequence(tokens, token_types.If):
            raise NotImplementedError()
        elif parse_utils.match_sequence(tokens, token_types.For):
            raise NotImplementedError()
        elif parse_utils.match_sequence(tokens, token_types.While):
            raise NotImplementedError()
        elif parse_utils.match_sequence(tokens, token_types.Id, token_types.Equal):
            return Assignment.parse(tokens)
        elif parse_utils.match_sequence(tokens, token_types.Integer):
            return ExprStatement.parse(tokens)
        parse_utils.unexpected_token(
            tokens.popleft(),
            token_types.If,
            token_types.For,
            token_types.While,
            token_types.Id,
            token_types.Integer,
        )


class ExprStatement(Statement):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    def __init__(self, expression: expression.Expression) -> None:
        self.expression = expression

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statement(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit(self.expression)

    def __eq__(self, other: ExprStatement) -> bool:
        return self.expression == other.expression


def parse_expr_statement(tokens: token.TokenStream) -> Statement:
    expr = expression.Expression.parse(tokens)
    parse_utils.expect(tokens, token_types.Semicolon)
    return ExprStatement(expr)


class Assignment(ExprStatement):
    """Represents an assignment of an expression to a variable."""

    def __init__(self, id: str, expression: expression.Expression) -> None:
        super().__init__(expression)
        self.id = id

    @staticmethod
    def parse(tokens: token.TokenStream) -> Assignment:
        id = parse_utils.expect(tokens, token_types.Id)
        parse_utils.expect(tokens, token_types.Equal)
        return Assignment(id.value, expression.Expression.parse(tokens))


class Declaration(Assignment):
    """Represents a variable declaration."""

    def __init__(self, id: str, expression: expression.Expression, const: bool) -> None:
        super().__init__(id, expression)
        self.const = const

    @staticmethod
    def parse(tokens: token.TokenStream) -> Declaration:
        if parse_utils.accept(tokens, token_types.Var):
            const = False
        elif parse_utils.accept(tokens, token_types.Const):
            const = True
        else:
            parse_utils.unexpected_token(
                tokens.popleft(), token_types.Var, token_types.Const
            )
        assignment = super().parse(tokens)
        return Declaration(assignment.id, assignment.expression, const)


class Control(Statement):
    """Represents a control structure like an if statement, function, or for loop."""

    def __init__(self, statements: Statements) -> None:
        self.statements = statements


class For(Control):
    pass
