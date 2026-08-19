# Robot Framework Exercises (FOTA)

Another iteration of the FOTA (Firmware Over-The-Air) socket-protocol Robot Framework exercise,
plus a small Fibonacci suite.

## Files

- `CustomSocketLibrary.py` — Custom Robot Framework library wrapping a TCP socket client.
- `server.py` — Mock FOTA target-device server (`run_fota_server`) on `127.0.0.1:8080`.
- `fota_tests.robot` — FOTA protocol test suite: successful/failed firmware update sequences,
  authentication with valid/invalid keys.
- `test_socket.robot` — Additional socket-based test suite.
- `Fib.robot` — Small, mostly-empty Fibonacci exercise suite.
- `runTest.bat` — Windows batch script to run the tests here.
- `log.html`, `output.xml`, `report.html` — Generated Robot Framework artifacts from a past run.

## Running

```powershell
python RobotFramworkExersize\server.py
robot RobotFramworkExersize\fota_tests.robot
```
