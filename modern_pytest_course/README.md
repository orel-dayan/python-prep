# Modern Pytest Course

A small example application (`app/`) with a matching test suite (`tests/`), used to practice
modern pytest patterns (fixtures, mocking, parametrize) against realistic-ish code. Has its own
`pytest.ini`, independent from the repo root config.

## `app/` — application code

- `cart.py` — `ShoppingCart` class: add/remove items, compute total and item count.
- `database.py` — `FakeDatabase`, an in-memory "database" that simulates a slow startup
  (`time.sleep`) to demonstrate expensive-fixture patterns (e.g. session-scoped fixtures).
- `file_db.py` — `FakeFileDatabase`, a JSON-file-backed database used to demonstrate fixtures
  that touch the filesystem (e.g. via `tmp_path`).
- `user.py` — `format_email()`: normalizes and validates an email address.
- `validation.py` — `is_valid_email()`: regex-based email format validation.

## `tests/` — test suite

- `test_cart.py`, `test_database.py`, `test_file_db.py`, `test_user.py`, `test_validation.py` —
  one test module per `app/` module, exercising each piece of functionality above.

## Running

```powershell
python -m pytest modern_pytest_course
```
