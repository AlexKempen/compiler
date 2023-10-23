from __future__ import annotations
from abc import ABC
from dataclasses import dataclass

from compiler.parse import node, visitor, parse_utils
from compiler.lex import token, token_type


class Expression(node.Node, ABC):
    """Represents an arithmetic or logical expression."""

    @staticmethod
    def parse(tokens: token.TokenStream, previous_precedence: int = 0) -> Expression:
        """Parses an expression."""
        from compiler.parse import literal

        if parse_utils.match_sequence(tokens, token_type.Id, token_type.LeftParens):
            left = Call.parse(tokens)
        # handle id case
        elif parse_utils.match(tokens, token_type.Integer):
            left = literal.IntegerLiteral.parse(tokens)
        else:
            parse_utils.unexpected_token(tokens, token_type.Id, token_type.Integer)

        while (
            tok := parse_utils.match(tokens, token.OperatorToken)
        ) and tok.PRECEDENCE > previous_precedence:
            tokens.popleft()  # Pop operator token
            right = Expression.parse(tokens, tok.PRECEDENCE)
            left = BinaryExpression(left, right, tok.value)

        return left


@dataclass
class Call(node.ParentNode, Expression):
    """Represents a function call.

    Call is a LogicalExpression since the return type is not typically inferred by the parser.
    """

    def __init__(self, id: str, *arguments: Expression):
        super().__init__(*arguments)
        self.id = id
        self.arguments = arguments

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_call(self)

    @staticmethod
    def parse(tokens: token.TokenStream) -> Call:
        id = parse_utils.expect(tokens, token_type.Id).value
        parse_utils.expect(tokens, token_type.LeftParens)
        arguments = []
        while not parse_utils.match(tokens, token_type.RightParens):
            arguments.append(Expression.parse(tokens))
            if not parse_utils.accept(tokens, token_type.Comma):
                break
        parse_utils.expect(tokens, token_type.RightParens)
        return Call(id, *arguments)


@dataclass
class BinaryExpression(node.ParentNode, Expression, ABC):
    """Represents an operation with two operands."""

    left: Expression
    right: Expression
    operator: str

    def __post_init__(self):
        super().__init__(self.left, self.right)

    def accept(self, visitor: visitor.Visitor) -> None:
        super().accept(visitor)
        visitor.visit_binary_expression(self)


class LogicalExpression(BinaryExpression):
    """An expression which operates on boolean values using a logical operator."""

    pass
