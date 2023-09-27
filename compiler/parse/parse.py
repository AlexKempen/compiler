from collections import deque
from typing import Iterable
from compiler.parse import node, expression
from compiler.scan import token


def parse(tokens: deque[token.Token]) -> node.Node:
    """Parses tokens into an AST comprised of Nodes."""
    return expression.parse_expression(tokens)
