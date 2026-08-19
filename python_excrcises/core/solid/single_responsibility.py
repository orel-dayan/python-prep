"""S — Single Responsibility: a class has one reason to change.

Device mixes two unrelated reasons to change: the wire protocol, and the log
format. A change to either forces editing the same class.
"""


class Device:
    def send_command(self, command: str) -> None:
        print(f"-> {command}")

    def write_log(self, message: str) -> None:
        with open("device.log", "a", encoding="utf-8") as f:
            f.write(message + "\n")


# Split by responsibility: each class changes for exactly one reason.
class DeviceGood:
    def send_command(self, command: str) -> None:
        print(f"-> {command}")


class FileLogger:
    def __init__(self, path: str):
        self.path = path

    def write(self, message: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(message + "\n")


if __name__ == "__main__":
    from pathlib import Path

    log_path = Path(__file__).with_name("_device.log")
    device = DeviceGood()
    logger = FileLogger(str(log_path))

    device.send_command("PING")
    logger.write("sent PING")
    print(log_path.read_text(encoding="utf-8"), end="")

    log_path.unlink()
