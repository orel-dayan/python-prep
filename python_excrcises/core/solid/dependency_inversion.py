"""D — Dependency Inversion: depend on an abstraction, not a concrete class.

TestRunnerBad constructs its own serial connection, so testing it means
opening a real port — impossible in CI, and slow even on a real bench.
"""

from typing import Protocol


class TestRunnerBad:
    def __init__(self):
        import serial

        self.connection = serial.Serial("/dev/ttyUSB0")  # hardware, no way around it

    def run(self) -> str:
        self.connection.write(b"PING")
        return "sent"


# The runner depends on an abstraction (anything with .write()), not a
# concrete serial port. A test passes in a fake; production passes in the
# real connection. Neither requires changing TestRunner.
class Connection(Protocol):
    def write(self, data: bytes) -> None: ...


class TestRunner:
    def __init__(self, connection: Connection):
        self.connection = connection

    def run(self) -> str:
        self.connection.write(b"PING")
        return "sent"


class FakeConnection:
    def __init__(self):
        self.sent: list[bytes] = []

    def write(self, data: bytes) -> None:
        self.sent.append(data)


if __name__ == "__main__":
    fake = FakeConnection()
    runner = TestRunner(fake)

    print(runner.run())
    print("bytes sent to the fake connection:", fake.sent)
