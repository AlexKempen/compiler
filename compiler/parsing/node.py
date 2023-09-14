from __future__ import annotations
from abc import ABC
from compiler.scanning import token, tokens


"""How to implement parsing?

1. Start with a root Node
Call rootNode.build(tokens)
rootNode iterates through its possible children and calls child.match(tokens) until it finds a valid match
Once it matches, that node is constructed using tokens, and the cycle repeats

So, there's two types of constructs:
A top level Node class, which has a list of possible children
And the children, which are also Nodes and have a utility for matching themselves against a stream of tokens?
"""


class Node(ABC):
    """Represents a node in an AST."""

    # Node, not Self, to avoid superclass restrictions
    def __init__(self, parent: Node):
        self.parent = parent

    # @classmethod
    # def match_next(cls, tokens: list[token.Token]) -> Node | None:
    #     subclasses = cls.__subclasses__()
    #     for cls in subclasses:
    #         next_match = cls.match_next(tokens)
    #         if next_match:
    #             return next_match
    #     return None


class BinaryNode(Node, ABC):
    """A node with two children."""

    def __init__(self, parent: Node, left: Node, right: Node):
        super().__init__(parent)
        self.left = left
        self.right = right


class UnaryNode(Node, ABC):
    """A node with a single child."""

    def __init__(self, parent: Node, child: Node):
        super().__init__(parent)
        self.child = child


PRECEDENCE: dict[type[token.Token], int] = {
    tokens.Plus: 12,
    tokens.Minus: 12,
    tokens.Times: 13,
    tokens.Divide: 13,
}


# class LeafNode(ABC):
#     """Represents a terminal node in the AST.

#     All tokens inherit from this class.
#     """

#     pass


# class Statement(Node):
#     """A statement node."""

#     pass


# class Expression(Node):
#     """An expression node."""

#     def __init__(self, parent: Node, expression: Expression):
#         super().__init__(parent)
#         self.expression = expression


# class Constant(Expression):
#     pass


# class Operator(Expression, ABC):
#     """An expression operation."""

#     def __init__(self):
#         pass


# class UnaryOperator(Operator, ABC):
#     pass


# class BooleanOperator(Operator, ABC):
#     pass


# class Add(BooleanOperator):
#     def __init__(self) -> None:
#         pass

#     @staticmethod
#     def match(toks: list[token.Token]) -> Add:
#         if isinstance(toks, tokens.Plus):
#             if toks[1] == tokens.Plus:
#                 return Add()


# class Multiply(BooleanOperator):
#     pass
