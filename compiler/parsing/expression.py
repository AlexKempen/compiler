from collections import deque
from compiler.parsing import node
from compiler.scanning import token


def get_precedence(tok: token.Token) -> int:
    if not isinstance(tok, token.OperatorToken):
        raise SyntaxError("Expected operator, got: {}".format(tok))
    return tok.PRECEDENCE


def parse_expression(
    tokens: deque[token.Token], previous_precedence: int = 0
) -> node.Expression:
    left = node.make_integer_node(tokens.popleft())

    if not tokens:
        return left

    while tokens and get_precedence(tokens[0]) > previous_precedence:
        op_token = tokens.popleft()  # tokens[0] is operator - remove it
        right = parse_expression(tokens, get_precedence(op_token))
        left = node.make_binary_operation(left, right, op_token)

    return left
