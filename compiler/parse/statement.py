from __future__ import annotations
from dataclasses import dataclass

from compiler.lex import token, token_type
from compiler.parse import expression, node, visitor, parse_utils


@dataclass
class Statements(node.ParentNode):
    """Represents a block of one or more statements in a row."""

    def __init__(self, *statements: Statement) -> None:
        self.statements = statements
        super().__init__(*statements)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statements(self)

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


@dataclass
class Statement(node.Node):
    """Represents a statement, a construct spanning one or more complete lines."""

    @staticmethod
    def parse(tokens: token.TokenStream) -> Statement:
        if parse_utils.match(tokens, token_type.If, token_type.For, token_type.While):
            raise NotImplementedError()
        elif parse_utils.match(tokens, token_type.Var, token_type.Const):
            return Declaration.parse(tokens)
        elif parse_utils.match_sequence(tokens, token_type.Id, token_type.Assign):
            return Assignment.parse(tokens)
        elif parse_utils.match(tokens, token_type.Integer, token_type.Id):
            return ExprStatement.parse(tokens)
        parse_utils.unexpected_token(
            tokens,
            token_type.If,
            token_type.For,
            token_type.While,
            token_type.Var,
            token_type.Const,
            token_type.Id,
            token_type.Integer,
        )


@dataclass
class ExprStatement(node.ParentNode, Statement):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    expression: expression.Expression

    def __post_init__(self) -> None:
        super().__init__(self.expression)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expr_statement(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> ExprStatement:
        expr = expression.Expression.parse(tokens)
        parse_utils.expect(tokens, token_type.Semicolon)
        return ExprStatement(expr)


@dataclass
class Assignment(ExprStatement):
    """Represents an assignment of an expression to a variable."""

    # expression inherited
    id: str

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_assignment(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Assignment:
        id = parse_utils.expect(tokens, token_type.Id).value
        parse_utils.expect(tokens, token_type.Assign)
        return Assignment(expression.Expression.parse(tokens), id)


@dataclass
class Declaration(node.ParentNode, Statement):
    """Represents a variable declaration, possibly with an initialization."""

    def __init__(
        self, id: str, const: bool, initialization: expression.Expression | None = None
    ) -> None:
        self.id = id
        self.const = const
        self.initialization = initialization

        if self.initialization:
            super().__init__(self.initialization)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Declaration:
        if parse_utils.accept(tokens, token_type.Var):
            const = False
        elif parse_utils.accept(tokens, token_type.Const):
            const = True
        else:
            # Technically should never happen...
            parse_utils.unexpected_token(tokens, token_type.Var, token_type.Const)
        id = parse_utils.expect(tokens, token_type.Id).value
        parse_utils.expect(tokens, token_type.Assign)

        init = None
        if not parse_utils.match(tokens, token_type.Semicolon):
            init = expression.Expression.parse(tokens)

        parse_utils.expect(tokens, token_type.Semicolon)
        return Declaration(id, const, init)


class Control(node.ParentNode, Statement):
    """Represents a control structure like an if statement, function, or for loop."""

    def __init__(self, statements: Statements) -> None:
        super().__init__(statements)
        self.statements = statements


class For(Control):
    pass
