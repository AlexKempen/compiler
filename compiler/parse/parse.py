from compiler.parse import statement
from compiler.lex import token, lex


def parse(tokens: token.TokenStream) -> statement.Statements:
    """Parses tokens into a Node AST."""
    return statement.Statements.parse(tokens)


def parse_code(code: str) -> statement.Statements:
    """Parses a code into a Node AST."""
    return parse(lex.lex(code))
