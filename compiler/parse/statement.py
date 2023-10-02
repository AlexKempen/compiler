from __future__ import annotations
from collections import deque
from compiler.lex import token, token_types

from compiler.parse import expression, node, visitor


class Statements(node.Node):
    """Matches one or more statements."""

    def __init__(self, *statements: Statement) -> None:
        self.statements = statements

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statements(self)


class Statement(node.Node):
    """Matches a single statement, consisting of an expression followed by a semicolon."""

    def __init__(self, expression: expression.Expression) -> None:
        self.expression = expression

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_statement(self)


def parse_statements(tokens: deque[token.Token]) -> Statements:
    statements = []
    while tokens:
        statements.append(parse_statement(tokens))
    return Statements(*statements)


def parse_statement(tokens: deque[token.Token]) -> Statement:
    statement = Statement(expression.parse_expression(tokens))
    tok = tokens.popleft()
    if not isinstance(tok, token_types.Semicolon):
        raise ValueError("Unexpected token - expected Semicolon, got: {}".format(tok))
    return statement
