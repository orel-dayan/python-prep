# Pytest Topics

Each pytest concept from `../test_examples.py` split into its own runnable file, for clarity.
Every file is self-contained: a module docstring explains the concept, followed by the example
code, with a "Run" command and expected result in the docstring itself.

## Files

| File | Topic |
|---|---|
| `test_01_assert_and_raises.py` | Plain `assert` + `pytest.raises` |
| `test_02_fixtures_yield_teardown.py` | Fixture setup/teardown via `yield` |
| `test_03_fixture_scope.py` | Fixture `scope` (module-scoped example) |
| `test_04_fixture_chaining_and_factory.py` | Fixtures depending on other fixtures; factory fixtures |
| `test_05_fixture_autouse_and_request.py` | `autouse=True` fixtures; the built-in `request` fixture |
| `test_06_markers.py` | `smoke`/`slow`/`skip`/`skipif`/`xfail` markers |
| `test_07_parametrize.py` | `@pytest.mark.parametrize` with `ids=` |
| `test_08_parametrize_indirect.py` | `parametrize(..., indirect=True)` |
| `test_09_mocking_unittest_mock.py` | Mocking with `unittest.mock` (`Mock` + `patch`) |
| `test_10_mocking_pytest_mock.py` | Mocking with the `mocker` fixture (from `pytest-mock`) |
| `test_11_builtin_fixtures.py` | `tmp_path`, `capsys`, `monkeypatch`, `caplog` |
| `test_12_approx.py` | `pytest.approx` for float comparisons |
| `test_13_skip_and_fail_runtime.py` | `pytest.skip()`/`pytest.fail()` called at runtime |
| `test_14_class_based_tests.py` | Class-based tests with `setup_method`/`teardown_method` |
| `test_15_failure_vs_error.py` | Failure (F) vs. Error (E) |
| `test_16_fixture_params.py` | `@pytest.fixture(params=...)` — a parametrized fixture |
| `test_17_pytest_warns.py` | `pytest.warns` — asserting a warning was raised |
| `test_18_mock_spec_and_autospec.py` | `Mock(spec=...)` / `create_autospec` — catching typos in mocks |
| `test_19_coverage_pytest_cov.py` | `pytest-cov` — measuring which lines your tests exercise |

## Running

```powershell
python -m pytest pytest_examples\topics -v          # run every topic file
python -m pytest pytest_examples\topics\test_06_markers.py -v   # run just one topic
```

`test_10_mocking_pytest_mock.py` needs `pytest-mock` (already installed in this project's
`.venv`). Without it, `mocker` errors with "fixture 'mocker' not found".

`test_19_coverage_pytest_cov.py` needs `pytest-cov` (also already installed) and the `--cov=`
flag shown in its docstring to produce a coverage table — running it without that flag just
runs the test normally, with no coverage report.

Note: `test_heavy_computation` (topic 06) and `test_resource_slow` (topic 05) are skipped by
default — the repo's root `../../conftest.py` auto-skips `@pytest.mark.slow` tests unless
`--runslow` is passed.
