from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from collections import deque
import re

T = TypeVar("T")


class Token(Generic[T], ABC):

    """Represents an atomic token.

    Attributes:
        value: The lexeme representing an instance of the class.
    """

    def __init__(self, value: T) -> None:
        self.value = value

    @classmethod
    def type(cls) -> str:
        """Returns the name of the type of this class."""
        return cls.__name__

    @classmethod
    @abstractmethod
    def match(cls, program: str) -> str | None:
        """Returns the part of the program matching this token and the corresponding value or None."""
        ...

    @staticmethod
    @abstractmethod
    def convert(match: str) -> T:
        ...

    def __repr__(self) -> str:
        """Used for debugging."""
        return repr(self.value)

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and self.value == other.value


class LiteralToken(Token[T], Generic[T], ABC):
    """Represents a literal token.

    Practically, this class represents a type of token which can be instantiated directly -
    the given literal type doesn't need any special handing.

    The convert method of LiteralToken is disregarded.
    """


class PatternToken(LiteralToken[str], ABC):
    """Represents a token which can be matched directly from the input.

    Many simple tokens fall into this category.
    Reserved keywords do not, since they must also be aware of what comes after.
    """

    PATTERN: str

    def __init__(self) -> None:
        super().__init__(self.PATTERN)

    @classmethod
    def type(cls) -> str:
        return cls.PATTERN

    @classmethod
    def match(cls, program: str) -> str | None:
        if not program.startswith(cls.PATTERN):
            return None
        return cls.PATTERN

    @staticmethod
    def convert(match: str) -> str:
        return match


def reserved_match(program: str, pattern: str) -> str | None:
    match = re.match(pattern + r"(?!\w)", program)
    return match.group(0) if match else None


class ReservedToken(PatternToken, ABC):
    """Represents a reserved token.

    Unlike a pattern token, no other Id characters are allowed to follow PATTERN.
    """

    @classmethod
    def match(cls, program: str) -> str | None:
        return reserved_match(program, cls.PATTERN)


class OperatorToken(PatternToken, ABC):
    """Represents an operator with an associated precedence."""

    PRECEDENCE: int


TokenStream = deque[Token]
"""An alias for a deque of tokens."""
