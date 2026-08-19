import pytest


def get_configured_port():
    """Simulates reading a configuration value from the environment."""
    import os
    return os.getenv("DEVICE_PORT", "COM1")

def is_valid_baud_rate(baud_rate):
    """Validates if the provided baud rate is within acceptable ranges."""
    return baud_rate in [9600, 19200, 38400, 57600, 115200]

class SerialConfig:
    """Represents a serial port configuration."""
    def __init__(self, baud_rate, parity):
        self.baud_rate = baud_rate
        self.parity = parity

    def is_valid(self):
        """Checks if the configuration is valid."""
        return is_valid_baud_rate(self.baud_rate) and self.parity in ["none", "even", "odd"]

def build_serial_config(baud_rate, parity):
    """Builds a SerialConfig object based on provided parameters."""
    return SerialConfig(baud_rate, parity)

def decode_ascii_byte(raw_byte):
    """Decodes a single byte to its ASCII character, returns None for non-printable bytes."""
    if 32 <= raw_byte <= 126:
        return chr(raw_byte)
    return None


def test_prints_status(capsys):
    """capsys captures stdout/stderr printed during the test."""
    print("READY")
    captured = capsys.readouterr()
    assert "READY" in captured.out


def test_uses_env_var(monkeypatch):
    """monkeypatch safely overrides env vars / attributes, reverted after the test."""
    monkeypatch.setenv("DEVICE_PORT", "COM3")
    assert get_configured_port() == "COM3"


def test_writes_log_file(tmp_path):
    """tmp_path gives a unique temporary directory, cleaned up automatically."""
    log_file = tmp_path / "results.log"
    log_file.write_text("PASS")
    assert log_file.read_text() == "PASS"
    
@pytest.mark.parametrize(
    ("baud_rate", "expected_valid"),
    [
        (9600, True),
        (115200, True),
        (0, False),
        (-1, False),
    ],
)
def test_baud_rate_validation(baud_rate, expected_valid):
    assert is_valid_baud_rate(baud_rate) == expected_valid
    
# cartesian product of parameters 
@pytest.mark.parametrize("baud_rate", [9600, 115200])
@pytest.mark.parametrize("parity", ["none", "even", "odd"])
def test_serial_config_combinations(baud_rate, parity):
    # Runs 6 times: 2 baud rates x 3 parity options
    config = build_serial_config(baud_rate, parity)
    assert config.is_valid()
    
    
@pytest.mark.parametrize(
    ("raw_byte", "expected"),
    [(0x41, "A"), (0x00, None), (0xFF, None)],
    ids=["printable-A", "null-byte", "max-byte"],
)
def test_byte_decoding(raw_byte, expected):
    assert decode_ascii_byte(raw_byte) == expected