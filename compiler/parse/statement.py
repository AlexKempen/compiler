from __future__ import annotations
from dataclasses import dataclass
import warnings

from compiler.lex import token, token_type
from compiler.parse import expression, node, visitor, parse_utils


@dataclass
class Program(node.ParentNode):
    """Represents a block of one or more statements in a row."""

    def __init__(self, *body: Statement) -> None:
        self.body = body
        super().__init__(*body)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_program(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Program:
        """Recursively parses tokens into a program."""
        body = []
        while tokens:
            body.append(Statement.parse(tokens))
        return Program(*body)


@dataclass
class BlockStatement(node.ParentNode):
    def __init__(self, *body: Statement) -> None:
        self.body = body
        super().__init__(*body)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_block_statement(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> BlockStatement:
        body = []
        while tokens:
            body.append(Statement.parse(tokens))
        return BlockStatement(*body)


@dataclass
class Statement(node.Node):
    """Represents a statement, a construct spanning one or more complete lines."""

    @staticmethod
    def parse(tokens: token.TokenStream) -> Statement:
        if parse_utils.match(tokens, token_type.If, token_type.For, token_type.While):
            raise NotImplementedError()
        elif parse_utils.match(tokens, token_type.Var, token_type.Const):
            return VariableDeclaration.parse(tokens)
        elif parse_utils.match_sequence(tokens, token_type.Id, token_type.Assign):
            return Assignment.parse(tokens)
        elif parse_utils.match(tokens, token_type.Integer, token_type.Id):
            return ExpressionStatement.parse(tokens)
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
class ExpressionStatement(node.ParentNode, Statement):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    expression: expression.Expression

    def __post_init__(self) -> None:
        super().__init__(self.expression)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expression_statement(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> ExpressionStatement:
        expr = expression.Expression.parse(tokens)
        parse_utils.expect(tokens, token_type.Semicolon)
        return ExpressionStatement(expr)


@dataclass
class Assignment(ExpressionStatement):
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
class VariableDeclaration(node.ParentNode, Statement):
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
    def parse(tokens: token.TokenStream) -> VariableDeclaration:
        if parse_utils.accept(tokens, token_type.Var):
            const = False
        elif parse_utils.accept(tokens, token_type.Const):
            const = True
        else:
            parse_utils.unexpected_token(tokens, token_type.Var, token_type.Const)

        id = parse_utils.expect(tokens, token_type.Id).value

        parse_utils.expect(tokens, token_type.Assign)
        init = None
        if not parse_utils.match(tokens, token_type.Semicolon):
            init = expression.Expression.parse(tokens)

        if const and init == None:
            warnings.warn("Const variables must be initialized")

        parse_utils.expect(tokens, token_type.Semicolon)
        return VariableDeclaration(id, const, init)


class Control(node.ParentNode, Statement):
    """Represents a control structure like an if statement, function, or for loop."""

    def __init__(self, statements: Program) -> None:
        super().__init__(statements)
        self.statements = statements


class For(Control):
    pass
