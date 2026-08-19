"""LEGB scope rule, global/nonlocal, and closures."""

counter = 0


def increment_fixed() -> None:
    global counter  # without this, `counter += 1` raises UnboundLocalError:
    counter += 1    # assigning to a name anywhere in a function makes it local


def outer() -> int:
    count = 0

    def inner() -> None:
        nonlocal count  # use the ENCLOSING function's variable, not a new local
        count += 1

    inner()
    return count


def make_multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor  # the closure remembers `factor` after make_multiplier returns
    return multiply


if __name__ == "__main__":
    increment_fixed()
    print("global counter:", counter)
    print("closure over outer():", outer())

    double = make_multiplier(2)
    print("closure over factor=2:", double(5))
