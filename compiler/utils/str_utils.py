from typing import Iterable


def indent(string: str) -> str:
    """Indents the beginning of every line in string."""
    return "".join("  " + line for line in string.splitlines(True))


def quote(string: str) -> str:
    """Adds quotes around string."""
    return '"{}"'.format(string)


# def parens(string: str) -> str:
#     """Adds parentheses around string."""
#     return "({})".format(string)


# def lower_first(string: str) -> str:
#     """Lowercases the first letter in string."""
#     return string[0].lower() + string[1:]


# def upper_first(string: str) -> str:
#     """Uppercases the first letter in string.

#     Unlike capitalize(), this function ignores other words.
#     """
#     return string[0].upper() + string[1:]


def end_join(*lines: str, sep: str = "\n") -> str:
    """Joins each input line. sep is also append to the end of the string."""
    return sep.join(lines) + sep
