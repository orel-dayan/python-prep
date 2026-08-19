# PythonProject1

## Virtual Environment Setup

### 1. Create a virtual environment

In PowerShell:

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

In Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If script execution is blocked, run this command once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

After the virtual environment is active:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> If you do not have a `requirements.txt` file, install packages individually as needed.

### 4. Deactivate the virtual environment

```powershell
deactivate
```

## Repository Overview

This repository is a collection of Python learning/practice material, small utilities, and
test-automation exercises (pytest, Robot Framework). Top-level layout:

- `conftest.py`, `pytest.ini` — shared pytest configuration and fixtures for the whole repo
  (kept at the root because `pytest.ini` uses `testpaths = .` to discover tests everywhere).
- `vending_machine/` — a small vending machine simulation (`vending_machine.py`,
  `vending_machine_v1.py`) with its pytest test suites.
- `pytest_examples/` — standalone pytest teaching examples: fixtures, scopes, parametrize,
  mocking, markers, etc.
- `cli_tools/` — command-line utilities (`qa_tool.py`, `runner_cli.py`) plus `runTests.bat`
  for repeatedly running the test suite on Windows.
- `reports/` — generated test/run artifacts (`log.html`, `output.xml`, `results.json`).
- `docs/` — extra reference notes (`python_automation_cyber.md`).
- `misc/` — miscellaneous scratch files (`main.py`, `test.txt`).
- `example-cli/` — an example CLI application with sample user JSON data and its own tests.
- `Exrcise_string/` — string utility exercises with their own `pytest.ini` and tests.
- `modern_pytest_course/` — a small `app/` package (cart, database, file_db, user, validation)
  with a matching `tests/` suite, used as a modern pytest course example.
- `networking/` — DHCP client/server experiments (`dhcp_packet.py`, `dhcp_server.py`, `client.py`).
- `python_excrcises/` — Python exercises: `core/` for single-topic language exercises
  (generators, dataclasses, pathlib, typing, concurrency, etc.) and `automation_examples/`
  for realistic scripts grouped by domain (network, security, system, utils).
- `Robot-Examples/`, `robot-framework/`, `RobotFramworkExersize/` — Robot Framework test suites
  and supporting Python libraries/servers for socket- and board-based testing.
- `test_types/` — examples of test doubles (fakes, mocks, stubs) with their own `tests/` suite.
- `output/` — output/log directory used by some scripts or test runs.