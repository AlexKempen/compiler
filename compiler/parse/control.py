from __future__ import annotations
from abc import ABC

from dataclasses import dataclass
from compiler.parse import expression, node, parse_utils, statement
from compiler.lex import token, token_type


@dataclass
class Control(statement.Statement, ABC):
    def __init__(
        self, body: statement.Statement | statement.BlockStatement, *args: node.Node
    ) -> None:
        super().__init__(body, *args)
        self.body = body


@dataclass
class TestControl(Control, ABC):
    def __init__(
        self,
        test: expression.Expression,
        body: statement.Statement | statement.BlockStatement,
        *args: node.Node,
    ) -> None:
        super().__init__(body, test, *args)
        self.test = test


def parse_test(tokens: token.TokenStream) -> expression.Expression:
    parse_utils.expect(tokens, token_type.LeftParens)
    test = expression.Expression.parse(tokens)
    parse_utils.expect(tokens, token_type.RightParens)
    return test


@dataclass
class For(Control):
    def __init__(
        self,
        init: statement.Statement,
        test: statement.ExpressionStatement,
        update: statement.ExpressionStatement,
        body: statement.Statement | statement.BlockStatement,
    ):
        super().__init__(body, init, test, update)
        self.init = init
        self.test = test
        self.update = update

    @staticmethod
    def parse(tokens: token.TokenStream) -> For:
        parse_utils.expect_sequence(tokens, token_type.For, token_type.LeftParens)
        init = statement.Statement.parse(tokens)
        # FS says the init statement cannot be a const declaration statement
        if isinstance(init, statement.VariableDeclaration) and init.const:
            raise ValueError("For loop initializer cannot be const")
        test = statement.ExpressionStatement.parse(tokens)
        update = statement.ExpressionStatement.parse(tokens, require_semicolon=False)
        parse_utils.expect(tokens, token_type.RightParens)
        body = statement.parse_single_or_block_statement(tokens)
        return For(init, test, update, body)


# class ForIn(Control):
#     def __Init__(
#             self,
#             init: statement.Statement,
#             statements: statement.BlockStatement
#     )


class While(TestControl):
    @staticmethod
    def parse(tokens: token.TokenStream) -> While:
        parse_utils.expect(tokens, token_type.While)
        test = parse_test(tokens)
        body = statement.parse_single_or_block_statement(tokens)
        return While(test, body)


class If(statement.Statement):
    def __init__(
        self,
        test: expression.Expression,
        consequent: statement.Statement | statement.BlockStatement,
        alternate: Else | ElseIf | None = None,
    ) -> None:
        args = [test, consequent]
        if alternate:
            args.append(alternate)
        super().__init__(*args)
        self.test = test
        self.consequent = consequent
        self.alternate = alternate

    @staticmethod
    def parse(tokens: token.TokenStream) -> If:
        parse_utils.expect_sequence(tokens, token_type.If)
        test = parse_test(tokens)
        body = statement.parse_single_or_block_statement(tokens)
        alternate = parse_alternate(tokens)
        return If(test, body, alternate)


def parse_alternate(tokens: token.TokenStream) -> Else | ElseIf | None:
    if parse_utils.match_sequence(tokens, token_type.Else, token_type.If):
        return ElseIf.parse(tokens)
    elif parse_utils.match(tokens, token_type.Else):
        return Else.parse(tokens)
    return None


class ElseIf(If):
    @staticmethod
    def parse(tokens: token.TokenStream) -> ElseIf:
        parse_utils.expect_sequence(tokens, token_type.Else, token_type.If)
        test = parse_test(tokens)
        body = statement.parse_single_or_block_statement(tokens)
        alternate = parse_alternate(tokens)
        return ElseIf(test, body, alternate)


class Else(Control):
    @staticmethod
    def parse(tokens: token.TokenStream) -> Else:
        parse_utils.expect(tokens, token_type.Else)
        body = statement.parse_single_or_block_statement(tokens)
        return Else(body)
