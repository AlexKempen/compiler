from typing import Iterable


def subclasses(cls: type) -> Iterable[type]:
    """Returns the subclasses of the given class.

    Note this method is non-recursive.
    """
    return cls.__subclasses__()
