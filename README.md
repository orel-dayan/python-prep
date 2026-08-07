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
צודקת — הראיתי את הטעות ולא את התיקון. הנה:

```python
import pytest

def test_invalid_config_raises():
    # Only the raising line goes inside the with block
    with pytest.raises(ConfigurationError, match="missing field: timeout"):
        load_config("broken.yaml")
    # Any further assertion goes AFTER the block
```

ואם את רוצה לבדוק את החריגה עצמה לעומק, זה מה ש-`excinfo` נותן:

```python
def test_invalid_config_details():
    with pytest.raises(ConfigurationError) as excinfo:
        load_config("broken.yaml")

    # These run because they are outside the with block
    assert "timeout" in str(excinfo.value)
    assert excinfo.value.field_name == "timeout"
    assert isinstance(excinfo.value.__cause__, KeyError)   # checks 'raise ... from e'
```

**הכלל:** בתוך ה-`with` — רק השורה שאמורה לזרוק. כל אימות נוסף אחרי הבלוק, דרך `excinfo.value`.

ולגבי ה-escaping ב-`match`, גם שם לא נתתי תיקון:

```python
# BAD - the parentheses and dot are regex syntax, not literal characters
with pytest.raises(ValueError, match="invalid port (70000). must be 1-65535"):
    ...

# GOOD - escape the literal text
import re
with pytest.raises(ValueError, match=re.escape("invalid port (70000). must be 1-65535")):
    ...

# Or match a distinctive substring instead of the whole message
with pytest.raises(ValueError, match="invalid port"):
    ...
```

