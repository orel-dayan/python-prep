import socket

class CustomSocketLibrary:
    def __init__(self):
        self._sock = None

    def connect_to_socket_server(self, host: str, port: int, timeout: float = 5.0):
        """Establishes TCP socket connection to target host and port."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(float(timeout))
        self._sock.connect((host, int(port)))

    def send_socket_payload(self, payload: str):
        """Sends string payload converted to UTF-8 bytes."""
        if not self._sock:
            raise RuntimeError("Socket connection is not open!")
        self._sock.sendall(payload.encode('utf-8'))

    def receive_socket_data(self, buffer_size: int = 1024) -> str:
        """Reads data from socket. Raises socket.timeout if no data arrives."""
        if not self._sock:
            raise RuntimeError("Socket connection is not open!")
        data = self._sock.recv(int(buffer_size))
        return data.decode('utf-8')

    def set_socket_timeout(self, seconds: float):
        """Dynamically sets the socket read/write timeout."""
        if not self._sock:
            raise RuntimeError("Socket connection is not open!")
        self._sock.settimeout(float(seconds))

    def disconnect_socket(self):
        """Closes the active socket connection."""
        if self._sock:
            self._sock.close()
            self._sock = None