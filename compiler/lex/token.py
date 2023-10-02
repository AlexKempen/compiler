from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Generic, Self, TypeVar

import re

T = TypeVar("T")


class Token(Generic[T]):
    __metaclass__ = ABCMeta

    """Represents an atomic token.

    Attributes:
        PATTERN: A string used alongside the default implemention of match() method to match instances of the token.
        type: The name of the token. Defaults to the name of the class.
        value: The lexeme representing an instance of the class.
    """

    PATTERN: str

    def __init__(self, value: T) -> None:
        self.type = self.generate_type()
        self.value = value

    def __repr__(self) -> str:
        return "Token: {}, {}".format(self.type, self.value)

    def __eq__(self, other: Self) -> bool:
        return self.type == other.type and self.value == other.value

    @classmethod
    def generate_type(cls) -> str:
        """Returns the type of the class.

        The default implementation uses the class name.
        """
        return cls.__name__

    @classmethod
    def match(cls, program: str) -> str | None:
        """Returns the part of the program matching this token or None.

        The default implementation returns the result of passing PATTERN to re.match().
        """
        match = re.match(cls.PATTERN, program)
        return match.group(0) if match else None

    @staticmethod
    @abstractmethod
    def convert(match: str) -> T:
        """Converts an instance of match into a lexeme value."""
        ...


class StrToken(Token[str]):
    @staticmethod
    def convert(match: str) -> str:
        return match


class LiteralToken(StrToken):
    """Represents a literal token.

    Unlike a regular token, PATTERN is matched directly rather than being interpreted as regex.
    """

    def __init__(self) -> None:
        super().__init__(self.PATTERN)

    @classmethod
    def match(cls, program: str) -> str | None:
        return cls.PATTERN if program.startswith(cls.PATTERN) else None


class OperatorToken(LiteralToken):
    """A token which corresponds to a mathematical operation."""

    PRECEDENCE: int


def make_token(token_type: type[Token], match: str) -> Token:
    if issubclass(token_type, LiteralToken):
        return token_type()
    else:
        return token_type(token_type.convert(match))
