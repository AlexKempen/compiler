from collections import deque
from typing import Iterable
from compiler.parsing import node, expression
from compiler.scanning import token


def parse(tokens: deque[token.Token]) -> node.Node:
    """Parses tokens into an AST comprised of Nodes."""
    return expression.parse_expression(tokens)
