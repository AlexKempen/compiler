from compiler.parse import statement
from compiler.lex import token, lex


def parse(tokens: token.TokenStream) -> statement.Program:
    """Parses tokens into a Program."""
    return statement.Program.parse(tokens)


def parse_code(code: str) -> statement.Program:
    """Parses a code into a Node AST."""
    return parse(lex.lex(code))
