# Test Types (Test Doubles)

Examples demonstrating the different kinds of "test doubles" — fakes, mocks, stubs, and a
simulator — using a simple gate-access-control scenario and a weather client.

## Files

- `gate_controller.py` — `GateController`: production code under test. Given a "database"
  dependency with a `.query(tag_id)` method, decides `GATE_OPEN` or `ALARM`.
- `fake.py` — A **fake**: `FakeDatabase` backed by a real in-memory `set`, with genuine
  (simplified) logic instead of canned answers.
- `Stub_example.py` — A **stub**: `StubDatabase` that always returns the same canned answer,
  with no call verification.
- `mock_example.py` — A **mock** example using `unittest.mock.Mock` to stub return values and
  verify calls on the database dependency.
- `simulator.py` — A more elaborate **simulator**: models gate hardware state
  (`GateState` enum: closed/opening/open/closing/fault) and can mimic hardware failures via
  `GateFaultError`.
- `weather_client.py` — `WeatherClient`/`WeatherError`: fetches temperature data from an
  external API dependency, with retry logic — used as another subject for test doubles.
- `result_store.py` — `ResultStore`: persists test results to a JSON file (open/add/close),
  used together with `tests/conftest.py` fixtures.
- `test_doubles_demo.py` — Self-contained, runnable demo comparing Mock vs Stub vs Fake vs
  Simulator side by side (`python test_doubles_demo.py`).

## `tests/`

- `conftest.py` — Fixtures for `ResultStore` (function-scoped `store`, plus a `populated_store`
  built on top of it using `tmp_path`).
- `test_result_store.py` — Tests for `ResultStore`.
- `test_weather_client.py` — Tests for `WeatherClient`, likely using test doubles for the API.

## Running

```powershell
python -m pytest test_types
```
