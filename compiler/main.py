from compiler.lex import lex
from compiler.parse import parse
from compiler.generate import llvm

# from compiler.utils import arguments


def main():
    """The entrypoint for the compiler."""
    # args = arguments.get_args()

    program = "10 + 5 / 24"

    tokens = lex.lex(program)
    node = parse.parse(tokens)
    with open("test.ll", "w") as f:
        f.write(llvm.generate("temp.hmm", node))


if __name__ == "__main__":
    main()
