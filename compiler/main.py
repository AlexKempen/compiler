import io
from compiler.scanning import lex
from compiler.utils import arguments


def main():
    """The entrypoint for the compiler."""
    # args = arguments.get_args()

    # program = io.open(args.PROGRAM).read()
    program = "10 + 5 / 24 * alpha"

    for token in lex.lex(program):
        print(token)


if __name__ == "__main__":
    main()
