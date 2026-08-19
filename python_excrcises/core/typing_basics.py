"""Type hints in practice: modern syntax + Protocol for structural typing.

Annotations aren't enforced at runtime — their value comes from a checker
(mypy/pyright) and editor autocomplete.
"""

from collections.abc import Iterable
from typing import Protocol


def total_bytes(sizes: Iterable[int]) -> int:
    """Accept the widest usable type (Iterable), not just list[int]."""
    return sum(sizes)


class SupportsClose(Protocol):
    """Anything with a close() method matches — no shared base class needed."""

    def close(self) -> None: ...


def shutdown_all(resources: Iterable[SupportsClose]) -> None:
    for resource in resources:
        resource.close()


class FakeSocket:
    def close(self) -> None:
        print("socket closed")


if __name__ == "__main__":
    print(total_bytes(n * 2 for n in range(4)))
    shutdown_all([FakeSocket()])
