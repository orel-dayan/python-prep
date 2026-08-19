"""O — Open/Closed: open for extension, closed for modification.

run_test_bad must be EDITED every time a new device type is added. Each
edit risks breaking the branches that already worked.
"""

from abc import ABC, abstractmethod


def run_test_bad(device_type: str) -> str:
    if device_type == "serial":
        return "running serial test"
    elif device_type == "can":
        return "running CAN test"
    raise ValueError(f"unknown device type: {device_type}")


# A new device is a new class. Existing classes are never touched.
class DeviceTest(ABC):
    @abstractmethod
    def run(self) -> str: ...


class SerialTest(DeviceTest):
    def run(self) -> str:
        return "running serial test"


class CanTest(DeviceTest):
    def run(self) -> str:
        return "running CAN test"


if __name__ == "__main__":
    tests: list[DeviceTest] = [SerialTest(), CanTest()]
    for test in tests:
        print(test.run())
