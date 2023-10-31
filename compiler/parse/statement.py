from __future__ import annotations
from dataclasses import dataclass
import warnings

from compiler.lex import token, token_type
from compiler.parse import control, expression, node, visitor, parse_utils


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


def parse_single_or_block_statement(
    tokens: token.TokenStream,
) -> Statement | BlockStatement:
    if parse_utils.accept(tokens, token_type.LeftBrace):
        body = BlockStatement.parse(tokens)
        parse_utils.expect(tokens, token_type.RightBrace)
    else:
        # There's a special error here for variable declarations...
        body = Statement.parse(tokens)
        if isinstance(body, VariableDeclaration):
            raise ValueError("Body may not be a single variable declaration")
    return body


class Statement(node.ParentNode):
    """Represents a statement, a construct spanning one or more complete lines."""

    @staticmethod
    def parse(tokens: token.TokenStream) -> Statement:
        if parse_utils.match(tokens, token_type.If):
            return control.If.parse(tokens)
        if parse_utils.match(tokens, token_type.For):
            return control.For.parse(tokens)
        if parse_utils.match(tokens, token_type.While):
            return control.While.parse(tokens)
        elif parse_utils.match(tokens, token_type.LeftBrace):
            return BlockStatement.parse(tokens)
        elif parse_utils.match(tokens, token_type.Var, token_type.Const):
            return VariableDeclaration.parse(tokens)
        elif parse_utils.match_sequence(tokens, token_type.Id, token_type.Assign):
            return Assignment.parse(tokens)
        elif parse_utils.match(
            tokens,
            token_type.Integer,
            token_type.Boolean,
            token_type.Undefined,
            token_type.Id,
        ):
            return ExpressionStatement.parse(tokens)
        parse_utils.unexpected_token(
            tokens,
            token_type.If,
            token_type.For,
            token_type.While,
            token_type.LeftBrace,
            token_type.Var,
            token_type.Const,
            token_type.Id,
            token_type.Integer,
        )


@dataclass
class BlockStatement(Statement):
    """Represents a block of statements wrapped in curly braces."""

    def __init__(self, *body: Statement) -> None:
        super().__init__(*body)
        self.body = body

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_block_statement(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> BlockStatement:
        parse_utils.expect(tokens, token_type.LeftBrace)
        body = []
        while not parse_utils.accept(tokens, token_type.RightBrace):
            body.append(Statement.parse(tokens))
        return BlockStatement(*body)


@dataclass
class ExpressionStatement(Statement):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    expression: expression.Expression
    has_semicolon: bool = True

    def __post_init__(self) -> None:
        super().__init__(self.expression)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_expression_statement(self)

    @staticmethod
    def parse(
        tokens: token.TokenStream, require_semicolon: bool = True
    ) -> ExpressionStatement:
        expr = expression.Expression.parse(tokens)
        if require_semicolon:
            parse_utils.expect(tokens, token_type.Semicolon)
        return ExpressionStatement(expr, has_semicolon=require_semicolon)


# Dont' inherit from expression statement since expression statements
@dataclass
class Assignment(ExpressionStatement):
    """Represents an assignment of an expression to a variable."""

    # expression inherited from parent
    def __init__(
        self, expression: expression.Expression, id: str, has_semicolon: bool = True
    ):
        super().__init__(expression, has_semicolon)
        self.id = id

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_assignment(self)

    @staticmethod
    def parse(tokens: token.TokenStream, require_semicolon: bool = True) -> Assignment:
        """
        Args:
            require_semicolon: True if the parse should require a semicolon. Used to handle the special for loop update case.
        """
        id = parse_utils.expect(tokens, token_type.Id).value
        parse_utils.expect(tokens, token_type.Assign)
        expr = expression.Expression.parse(tokens)
        if require_semicolon:
            parse_utils.expect(tokens, token_type.Semicolon)
        return Assignment(expr, id, has_semicolon=require_semicolon)


@dataclass
class VariableDeclaration(Statement):
    """Represents a variable declaration, possibly with an initialization."""

    def __init__(
        self, id: str, const: bool, initialization: expression.Expression | None = None
    ) -> None:
        self.id = id
        self.const = const
        self.initialization = initialization

        if self.initialization:
            super().__init__(self.initialization)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_variable_declaration(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> VariableDeclaration:
        if parse_utils.accept(tokens, token_type.Var):
            const = False
        elif parse_utils.accept(tokens, token_type.Const):
            const = True
        else:
            parse_utils.unexpected_token(tokens, token_type.Var, token_type.Const)

        id = parse_utils.expect(tokens, token_type.Id).value

        init = None
        if not parse_utils.match(tokens, token_type.Semicolon):
            parse_utils.expect(tokens, token_type.Assign)
            init = expression.Expression.parse(tokens)

        if const and init == None:
            warnings.warn("Const variables must be initialized")

        parse_utils.expect(tokens, token_type.Semicolon)
        return VariableDeclaration(id, const, init)
