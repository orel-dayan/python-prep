# Robot Examples

Robot Framework tests for an embedded board communicating over serial, plus a socket-based
mock/test server.

## Files

- `board_library.py` — Custom Robot Framework library (`BoardLibrary`) that talks to an
  embedded board over a serial connection (`connect_to_board`, `send_command`, etc.).
- `board_tests.robot` — Robot test suite using `board_library.py`: connects to a board over
  serial (`/dev/ttyUSB0`), sends commands (e.g. `PING`), and checks responses/status.
- `CustomSocketLibrary.py` — Custom Robot Framework library for talking to a TCP socket server
  (`connect_to_socket_server`, `send_socket_payload`, ...).
- `server.py` — A mock TCP server simulating device responses (status, temperature, version)
  used by the socket-based tests.
- `example.robot`, `test_socket.robot` — Additional Robot Framework test suites exercising the
  socket server/library.
- `report.html` — Generated Robot Framework HTML report from a past run.

## Running

```powershell
robot Robot-Examples\board_tests.robot
```
