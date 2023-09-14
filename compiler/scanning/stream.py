"""Unused stream classes."""

from abc import ABC, abstractmethod


class Stream(ABC):
    """A basic interface for working with a stream of characters."""

    @abstractmethod
    def eof(self) -> bool:
        """Returns true if the end of the file is reached."""
        ...

    @abstractmethod
    def next(self) -> str:
        """Reads the next character."""
        ...

    @abstractmethod
    def peek(self) -> str:
        """Accesses the next character without reading it."""
        ...


class StringStream(Stream):
    """An implementation of Stream on a standard string."""

    def __init__(self, string: str) -> None:
        self.string = string
        self.curr = 0

    def eof(self) -> bool:
        return self.curr == len(self.string)

    def next(self) -> str:
        next = self.string[self.curr]
        self.curr += 1
        return next

    def peek(self) -> str:
        return self.string[self.curr]
