from compiler.lex import lex
from compiler.parse import parse
from compiler.generate import llvm

# from compiler.utils import arguments


def main():
    """The entrypoint for the compiler."""
    program = "print(3 + 2 * 2); print(2 + 1);"

    tokens = lex.lex(program)
    node = parse.parse(tokens)
    llvm_code = llvm.generate(node)
    print(llvm.execute(llvm_code))


if __name__ == "__main__":
    main()
