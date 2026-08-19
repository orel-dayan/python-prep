import random
import socket


def handle_sys_status() -> bytes:
    return b"STATUS=OK\n"


def handle_temperature() -> bytes:
    # Simulate a temperature reading
    temp = round(random.uniform(35.0, 45.0), 1)
    return f"TEMP={temp}\n".encode()


def handle_version() -> bytes:
    return b"VERSION=1.0.3\n"


def handle_ping() -> bytes:
    return b"PONG\n"


def handle_reset() -> bytes:
    return b"STATUS=RESETTING\n"


# Command dispatch table: maps each supported command to its handler function
COMMAND_HANDLERS = {
    "GET_SYS_STATUS": handle_sys_status,
    "GET_TEMPERATURE": handle_temperature,
    "GET_VERSION": handle_version,
    "PING": handle_ping,
    "RESET": handle_reset,
}


def build_response(command: str) -> bytes:
    """Builds a simulated hardware response for a given command."""
    command = command.strip()

    if command == "":
        return b""

    handler = COMMAND_HANDLERS.get(command)
    if handler is None:
        return b"ERROR=UNKNOWN_COMMAND\n"

    return handler()


def handle_client(conn, addr):
    """Handles a single client connection, supporting multiple commands
    over the same connection until the client disconnects."""
    print(f"Client connected: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                # Client closed the connection
                break

            command = data.decode('utf-8')
            print(f"Received command from Robot: {command.strip()}")

            response = build_response(command)
            if response:
                conn.sendall(response)
                print(f"Sent response: {response!r}")

    print(f"Client disconnected: {addr}")


def run_mock_server():
    # Bind to localhost on port 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen(1)
    print("Mock Hardware Server listening on 127.0.0.1:8080...")

    try:
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nShutting down mock server.")
    finally:
        server.close()


if __name__ == '__main__':
    run_mock_server()