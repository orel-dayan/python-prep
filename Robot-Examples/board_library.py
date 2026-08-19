"""Custom Robot Framework library for communicating with an embedded board over serial."""

import time

import serial


class BoardLibrary:
    """Custom Robot Framework library for communicating with an embedded board over serial."""

    def __init__(self):
        self.connection = None

    def connect_to_board(self, port, baudrate=115200):
        """Opens a serial connection to the board."""
        self.connection = serial.Serial(port, baudrate, timeout=2)
        time.sleep(0.5)  # allow board to reset after connection

    def send_command(self, command):
        """Sends a text command to the board, terminated with newline."""
        self.connection.write((command + "\n").encode())

    def read_response(self):
        """Reads a single line response from the board."""
        return self.connection.readline().decode().strip()

    def close_connection(self):
        """Closes the serial connection."""
        if self.connection:
            self.connection.close()
