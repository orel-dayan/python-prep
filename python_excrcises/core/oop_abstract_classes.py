"""OOP in Python -- the four pillars (encapsulation, inheritance, polymorphism,
abstraction) built around one example: an abstract `Shape` base class.

Abstract base class rules (via `abc.ABC` / `abc.abstractmethod`):
- A class becomes abstract by inheriting from `ABC` (or using `metaclass=ABCMeta`).
- `@abstractmethod` marks a method the subclass MUST override.
- Python refuses to instantiate any class that still has unimplemented
  abstract methods -- `Shape()` raises `TypeError`, not just a lint warning.
- An abstract class can still define concrete (regular) methods, `__init__`,
  and even abstract *properties* (`@property` stacked above `@abstractmethod`).
- A subclass only becomes instantiable once it implements every abstract member.
"""

from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstraction: defines *what* every shape can do, not *how*."""

    def __init__(self, name: str):
        self._name = name  # encapsulation: internal state exposed via a property

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def area(self) -> float:
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        # concrete method: shared by every subclass, built on the abstract ones
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):  # inheritance: reuses Shape's __init__, name, describe
    def __init__(self, radius: float):
        super().__init__("Circle")
        self._radius = radius

    def area(self) -> float:
        return 3.14159 * self._radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self._radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self._width = width
        self._height = height

    def area(self) -> float:
        return self._width * self._height

    def perimeter(self) -> float:
        return 2 * (self._width + self._height)


if __name__ == "__main__":
    shapes: list[Shape] = [Circle(3), Rectangle(4, 5)]

    for shape in shapes:  # polymorphism: same call, different behavior per subclass
        print(shape.describe())

    try:
        Shape("x")  # abstract class rule: cannot instantiate directly
    except TypeError as e:
        print(e)
