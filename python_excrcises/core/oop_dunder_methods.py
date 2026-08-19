"""__repr__ and __eq__ — the two dunder methods worth defining on almost
every plain class (a @dataclass generates both for you automatically;
see dataclasses_guide.py).
"""


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        # Convention: repr should look like the code that recreates the object.
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


if __name__ == "__main__":
    a, b = Point(1, 2), Point(1, 2)
    print(a)
    print(a == b)
