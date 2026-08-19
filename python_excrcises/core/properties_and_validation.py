"""@property — validate on assignment without changing the calling code."""


class Person:
    def __init__(self, name: str):
        self.name = name
        self._age: int | None = None

    @property
    def age(self) -> int | None:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value


if __name__ == "__main__":
    p = Person("Alice")
    p.age = 30
    print(p.name, p.age)

    try:
        p.age = -5
    except ValueError as e:
        print(e)
