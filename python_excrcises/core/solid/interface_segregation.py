"""I — Interface Segregation: many small interfaces beat one big one.

Device forces every implementation to define calibrate(), even a read-only
sensor that has nothing to calibrate.
"""

from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def read(self) -> float: ...

    @abstractmethod
    def write(self, value: float) -> None: ...

    @abstractmethod
    def calibrate(self) -> None: ...


# Split by capability. A class implements only what it actually supports.
class Readable(ABC):
    @abstractmethod
    def read(self) -> float: ...


class Writable(ABC):
    @abstractmethod
    def write(self, value: float) -> None: ...


class ReadOnlySensor(Readable):
    def read(self) -> float:
        return 21.5


class Actuator(Readable, Writable):
    def __init__(self):
        self._value = 0.0

    def read(self) -> float:
        return self._value

    def write(self, value: float) -> None:
        self._value = value


if __name__ == "__main__":
    sensor = ReadOnlySensor()
    actuator = Actuator()

    print("sensor reading:", sensor.read())
    actuator.write(3.3)
    print("actuator reading:", actuator.read())
