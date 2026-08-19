# Robot Framework (FOTA Socket Tests)

Robot Framework tests for a simulated FOTA (Firmware Over-The-Air) update protocol over TCP
sockets.

## Files

- `CustomSocketLibrary.py` — Custom Robot Framework library wrapping a TCP socket client
  (connect, send payload, disconnect, etc.).
- `server.py` — Mock FOTA target-device server (`run_fota_server`) listening on
  `127.0.0.1:8080`, simulating authentication and firmware-flashing state transitions.
- `fotav1_tests.robot` — FOTA protocol test suite: authentication with a valid/invalid key,
  firmware update sequence, using `CustomSocketLibrary.py` and the `String` library.
- `test_socket.robot` — Additional socket-based test suite.
- `r.robot` — Minimal/scratch Robot Framework suite.
- `runTest.bat` — Windows batch script to run the Robot Framework tests here.

## Running

Start the mock server, then run the tests:

```powershell
python robot-framework\server.py
robot robot-framework\fotav1_tests.robot
```
