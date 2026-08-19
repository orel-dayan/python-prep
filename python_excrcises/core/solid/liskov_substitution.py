"""L — Liskov Substitution: a subclass must honor its parent's contract.

Anywhere a Bird is expected, a Penguin should work too. Penguin breaks that
promise: calling fly() on what the caller believes is "just a Bird" crashes.
"""


class Bird:
    def fly(self) -> str:
        return "flying"


class Penguin(Bird):
    def fly(self) -> str:
        raise NotImplementedError("penguins can't fly")  # violates the contract


def make_it_fly(bird: Bird) -> str:
    return bird.fly()  # any Bird should work here — that's the whole point of the type


# Fix: don't model "can't fly" as an override that lies. Split the capability
# out of the base type so the type system reflects reality.
class FlightlessBird:
    def walk(self) -> str:
        return "walking"


class PenguinGood(FlightlessBird):
    pass


if __name__ == "__main__":
    print(make_it_fly(Bird()))

    try:
        make_it_fly(Penguin())
    except NotImplementedError as e:
        print(f"broke the contract: {e}")

    print(PenguinGood().walk())  # no longer pretends to be a flying Bird
