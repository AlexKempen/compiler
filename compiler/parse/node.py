from __future__ import annotations
from abc import ABC

from compiler.lex import token
from compiler.parse import visitor
from compiler.utils import str_utils


class Node(ABC):
    """Represents a node in an AST."""

    # def accept(self, visitor: visitor.Visitor) -> None:
    #     cls = self.__class__
    #     while cls != None:
    #         name = cls.__name__
    #         visit_function_name = "visit_" + str_utils.camel_case_to_snake_case(name)
    #         print("Call {}".format(visit_function_name))
    #         visit_function = getattr(visitor, visit_function_name)
    #         visit_function(self)
    #         cls = super()

    def accept(self, visitor: visitor.Visitor) -> None:
        """Accepts a given visitor, executing the appropriate method."""
        visitor.visit_node(self)

    # Not abstract since isn't strictly required
    @staticmethod
    def parse(tokens: token.TokenStream) -> Node:
        """Parses a stream of tokens into the given Node."""
        raise NotImplementedError()


class ParentNode(Node):
    def __init__(self, *children: Node) -> None:
        self.children = children
