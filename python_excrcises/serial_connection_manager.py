from typing import Optional

try:
    import serial
except ModuleNotFoundError:
    class SerialException(Exception):
        pass

    class Serial:
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError("pyserial is required for serial communication")

    class _SerialFallback:
        EIGHTBITS = 8
        PARITY_NONE = "N"
        STOPBITS_ONE = 1
        Serial = Serial
        SerialException = SerialException

    serial = _SerialFallback()


class SerialDeviceCommunicator:
    """
    A robust wrapper around pyserial for hardware communication.
    Supports context management, timeout handling, and line-based framing.
    """
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._ser: Optional[serial.Serial] = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self) -> None:
        """Opens the serial port with the configured parameters."""
        try:
            self._ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            # Clear input and output buffers
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()
            print(f"[SERIAL] Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"[ERROR] Failed to open port {self.port}: {e}")
            raise

    def send_command(self, command: str) -> None:
        """
        Encodes string command to bytes and appends newline delimiter.
        """
        if not self._ser or not self._ser.is_open:
            raise RuntimeError("Serial port is not open.")
        
        # Framing: Append '\n' delimiter and convert to bytes
        formatted_cmd = (command.strip() + "\n").encode('utf-8')
        self._ser.write(formatted_cmd)
        self._ser.flush()  # Ensure all bytes are written to hardware
        print(f"[TX -> {self.port}] {command}")

    def read_response(self) -> str:
        """
        Reads until '\n' delimiter or until timeout expires.
        """
        if not self._ser or not self._ser.is_open:
            raise RuntimeError("Serial port is not open.")

        # readline() reads until '\n' or timeout
        raw_bytes = self._ser.readline()
        
        if not raw_bytes:
            raise TimeoutError(f"No response received from {self.port} within {self.timeout}s")

        decoded_str = raw_bytes.decode('utf-8', errors='replace').strip()
        print(f"[RX <- {self.port}] {decoded_str}")
        return decoded_str

    def close(self) -> None:
        """Closes the serial port cleanly."""
        if self._ser and self._ser.is_open:
            self._ser.close()
            print(f"[SERIAL] Port {self.port} closed.")