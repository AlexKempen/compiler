from __future__ import annotations
from abc import ABC

from compiler.lex import token
from compiler.parse import visitor
from compiler.utils import str_utils


class Node(ABC):
    """Represents a node in an AST."""

    def accept(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor."""
        visitor.visit_node(self)

    # def accept_helper(self, visitor: visitor.Visitor) -> None:
    #     """Automatically invokes the correct method on visitor."""
    #     class_name = self.__class__.__name__
    #     visit_method_name = "visit_{}".format(str_utils.camel_to_snake_case(class_name))
    #     visit_method = getattr(visitor, visit_method_name)
    #     visit_method(self)

    # Not abstract since isn't strictly required
    @staticmethod
    def parse(tokens: token.TokenStream) -> Node:
        """Parses a stream of tokens into the given Node."""
        raise NotImplementedError()


class ParentNode(Node):
    def __init__(self, *children: Node) -> None:
        self.children = children
