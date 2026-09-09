# Modern Pytest Course

A small example application (`app/`) with a matching test suite (`tests/`), used to practice
modern pytest patterns (fixtures, mocking, parametrize) against realistic-ish code. Has its own
`pytest.ini`, independent from the repo root config.

## `app/` — application code

- `cart.py` — `ShoppingCart` class: add/remove items, compute total and item count.
- `database.py` — `FakeDatabase`, an in-memory "database" that simulates a slow startup
  (`time.sleep`) to demonstrate expensive-fixture patterns (e.g. session-scoped fixtures).
- `data_processor.py` — `fast_sum()` and `slow_report()` (the latter sleeps to simulate a slow
  operation), used to demonstrate testing/mocking of slow computations.
- `file_db.py` — `FakeFileDatabase`, a JSON-file-backed database used to demonstrate fixtures
  that touch the filesystem (e.g. via `tmp_path`).
- `http_status.py` — `get_status_message()`: maps an HTTP status code to its message using
  `match`/`case` (requires Python 3.10+).
- `shipping.py` — `calculate_shipping()`: tiered shipping fee/discount/free-shipping logic based
  on order total.
- `user.py` — `format_email()`: normalizes and validates an email address.
- `user_service.py` — `send_email()` and `register_user()`: registration flow with a "side
  effect" dependency (`send_email`) meant to be mocked/monkeypatched in tests.
- `validation.py` — `is_valid_email()`: regex-based email format validation.

## `tests/` — test suite

- `conftest.py` — adds the project root to `sys.path` so `app` is importable regardless of the
  directory pytest is invoked from.
- `test_cart.py`, `test_database.py`, `test_data_processor.py`, `test_file_db.py`,
  `test_shipping.py`, `test_user.py`, `test_validation.py` — one test module per `app/` module,
  exercising each piece of functionality above.
- `test_skipif.py` — demonstrates `@pytest.mark.skipif` for platform- and
  Python-version-conditional tests.
- `test_user_service.py`, `test_user_service_boolean_flag.py` — demonstrate mocking/monkeypatching
  `send_email` in `user_service.register_user()`.

## Running

```powershell
python -m pytest modern_pytest_course
```
