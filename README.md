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

---

## Project Overview

- `main.py` - main entry point
- `test_*.py` - pytest test files
- `runTests.bat` - Windows batch script for running tests
