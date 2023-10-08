from compiler.lex import lex
from compiler.parse import parse
from compiler.generate import llvm

# from compiler.utils import arguments


def main():
    """The entrypoint for the compiler."""
    program = "print(3 + 2 * 2); print(2 + 1);"

    node = parse.parse_code(program)
    print(llvm.execute_node(node))


if __name__ == "__main__":
    main()
