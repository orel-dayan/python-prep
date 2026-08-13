class Person:
    def __init__(self, name: str):
        self.name: str = name
        self._age: int

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int):
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value


def main() -> None:
    try:
        p = Person("Alice")
        p.age = -5  # This will raise a ValueError
        print(f"Name: {p.name}, Age: {p.age}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
