from typing import Iterable
from compiler.scanning import token
from compiler.parsing import node


def parse(tokens: Iterable[token.Token]) -> node.Node:
    """Parses tokens into an AST comprised of Nodes."""
    # return Node()
    pass
