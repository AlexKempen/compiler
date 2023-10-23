from abc import ABC
from typing import Iterable


def subclasses(cls: type) -> Iterable[type]:
    """Returns the non-abstract immediate subclasses of the given class.

    Note this method is non-recursive.
    """
    for temp in cls.__subclasses__():
        yield temp


def all_subclasses(cls: type) -> Iterable[type]:
    """Returns all non-abstract subclasses of the given class."""
    for temp in cls.__subclasses__():
        yield from _all_subclasses(temp)


def _all_subclasses(cls: type) -> Iterable[type]:
    if cls.__subclasses__() == []:
        yield cls
    for temp in cls.__subclasses__():
        yield from _all_subclasses(temp)
