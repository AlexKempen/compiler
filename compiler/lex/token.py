from __future__ import annotations
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass

from typing import Any, Generic, TypeVar

import re


T = TypeVar("T")


class Token(Generic[T], ABC):

    """Represents an atomic token.

    Attributes:
        PATTERN: A string used alongside the default implemention of match() method to match instances of the token.
        value: The lexeme representing an instance of the class.
    """

    PATTERN: str

    def __init__(self, value: T) -> None:
        self.value = value

    @classmethod
    def type(cls) -> str:
        """Returns the name of the type of this class."""
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

    def __repr__(self) -> str:
        return repr(self.value)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Token) and self.value == other.value


class LiteralToken(Token[str], ABC):
    """Represents a literal token.

    Unlike a regular token, PATTERN is matched directly rather than being interpreted as regex.
    """

    def __init__(self) -> None:
        super().__init__(self.PATTERN)

    @classmethod
    def type(cls) -> str:
        return cls.PATTERN

    @classmethod
    def match(cls, program: str) -> str | None:
        return cls.PATTERN if program.startswith(cls.PATTERN) else None

    @staticmethod
    def convert(match: str) -> str:
        return match


class ReservedToken(Token[T], Generic[T], ABC):
    """Represents a reserved token.

    Unlike a literal token, the entire LiteralToken must match, and no other Id characters are allowed to follow.
    """

    VALUE: T

    def __init__(self) -> None:
        super().__init__(self.VALUE)

    @classmethod
    def type(cls) -> str:
        return cls.PATTERN

    @classmethod
    def match(cls, program: str) -> str | None:
        match = re.match(cls.PATTERN + r"(?!\w)", program)
        return match.group(0) if match else None


class StrReservedToken(ReservedToken[str]):
    def __init__(self) -> None:
        Token.__init__(self, self.PATTERN)


class OperatorToken(LiteralToken, ABC):
    """Represents an operator, with an associated precedence."""

    PRECEDENCE: int


TokenStream = deque[Token]
"""An alias for a deque of tokens."""
