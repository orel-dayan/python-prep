# Pytest Examples

Standalone teaching/reference files for pytest features, not tied to any specific application
module.

## Files

- `test_examples.py` — Comprehensive pytest reference: `assert`, `pytest.raises`, fixtures
  (scope/chaining/factories/autouse), the `request` fixture, markers (smoke/slow/skip/skipif/xfail),
  `parametrize` (with ids and indirect), mocking (`unittest.mock` and `pytest-mock`), built-in
  fixtures (`tmp_path`, `capsys`, `monkeypatch`, `caplog`), `pytest.approx`, class-based tests,
  and the difference between test failures and errors.
- `test_fixtures_examples.py` — Focused examples of fixture scopes (function/class/module/session)
  and fixture composition.
- `test_practice.py` — General pytest practice exercises.
- `test_scope.py` — Examples around fixture scope and configuration-reading patterns
  (e.g. simulating environment-based config with `os.getenv`).
- `topics/` — The same concepts from `test_examples.py`, split into one small, runnable file
  per topic for clarity. See [topics/README.md](topics/README.md).

## Running

```powershell
python -m pytest pytest_examples -v
```

For a full pytest walkthrough (fixtures, scopes, markers, `parametrize`, mocking, built-in
fixtures, and more, with deep explanations), see [PYTEST_TUTORIAL.md](PYTEST_TUTORIAL.md).
