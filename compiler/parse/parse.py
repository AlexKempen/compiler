from collections import deque
from compiler.parse import node, statement
from compiler.lex import token


def parse(tokens: deque[token.Token]) -> statement.Statements:
    """Parses tokens into an AST comprised of Nodes."""
    return statement.parse_statements(tokens)
