from __future__ import annotations
from collections import deque
from compiler.lex import token, token_types

from compiler.parse import expression, node, visitor, parse_utils


class Statements(node.Node):
    """Matches one or more statements."""

    def __init__(self, *statements: Statement) -> None:
        self.statements = statements

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statements(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit_all(*self.statements)

    def __eq__(self, other: Statements) -> bool:
        return self.statements == other.statements


def parse_statements(tokens: deque[token.Token]) -> Statements:
    """Recursively parses tokens into a list of statements.

    Currently terminates at eof.
    In the future, statements will also terminate at the end of a block (}).
    """
    statements = []
    while tokens:
        statements.append(parse_statement(tokens))
    return Statements(*statements)


class Statement(node.Node):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    def __init__(self, expression: expression.Expression) -> None:
        self.expression = expression

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statement(self)

    def accept_children(self, visitor: visitor.Visitor) -> None:
        visitor.visit(self.expression)

    def __eq__(self, other: Statement) -> bool:
        return self.expression == other.expression


def parse_statement(tokens: deque[token.Token]) -> Statement:
    expr = expression.parse_expression(tokens)
    parse_utils.assert_token(tokens.popleft(), token_types.Semicolon)
    return Statement(expr)
