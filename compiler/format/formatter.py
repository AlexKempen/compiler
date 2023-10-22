from compiler.format import format_visitor
from compiler.parse import parse


def format(program: str) -> str:
    """Formats program."""
    node = parse.parse_code(program)
    return format_visitor.FormatVisitor().visit(node)
