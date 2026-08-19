# Pytest Tutorial — full walkthrough

This is a deep, from-scratch explanation of every pytest concept used across the codebase, with
references to the files where you can see each one in action.

## 1. The basics: `assert` and test discovery

Pytest uses plain `assert` statements — no `self.assertEqual(...)` needed. Under the hood,
pytest **rewrites** `assert` statements at import time (via an import hook), replacing a bare
`assert a == b` with code that captures both sides and prints a detailed diff on failure. This
is why `assert` in a pytest test gives rich output, while the exact same `assert` in a plain
script just raises a bare `AssertionError`.

Discovery rules (configurable in `pytest.ini`):
- Files matching `test_*.py` or `*_test.py` (`python_files`).
- Functions/methods starting with `test_` (`python_functions`).
- Classes starting with `Test`, with **no `__init__`** — pytest silently skips classes that
  define `__init__` because it can't instantiate them the way it needs to (`python_classes`).
- `testpaths` in `pytest.ini` narrows *where* pytest looks by default when run with no
  arguments (this repo's root `pytest.ini` uses `testpaths = .`, so it scans the whole tree).

## 2. Running tests

```powershell
python -m pytest                     # run everything under testpaths
python -m pytest path\to\file.py     # run one file
python -m pytest file.py::test_name  # run one test function
python -m pytest file.py::TestClass::test_name  # run one method in a class
python -m pytest -k "smoke"          # run tests matching a keyword expression (name substring/boolean)
python -m pytest -m smoke            # run tests matching a marker
python -m pytest -v                  # verbose (show each test name)
python -m pytest -s                  # don't capture stdout (show print())
python -m pytest -x                  # stop after the first failure
python -m pytest --lf                # rerun only the tests that failed last time
python -m pytest --ff                # run previously-failed tests first, then the rest
python -m pytest --collect-only      # list what would run, without running it
```

`-k` accepts boolean expressions, e.g. `-k "smoke and not slow"`.

## 3. Fixtures

A fixture is a function decorated with `@pytest.fixture` that provides setup (and optional
teardown) for tests. Tests receive it by naming it as a parameter — pytest resolves the
dependency graph and calls the fixture function for you; you never call it directly.

```python
@pytest.fixture
def vending_machine():
    return VendingMachine()

def test_initial_state(vending_machine):
    assert vending_machine.inserted_money == 0
```
(see `../vending_machine/test_vending_machine.py`)

### Setup + teardown with `yield`

Code before `yield` is setup; code after is teardown. The teardown code runs even if the test
fails or raises, because pytest treats the generator's cleanup like a `finally` block:

```python
@pytest.fixture
def tmp_file():
    def create(contents=""):
        ...
        return path
    yield create
    # cleanup runs here, after the test finishes — even on failure
```
(see `test_scope.py`)

An older, less common style uses `request.addfinalizer(callback)` instead of `yield` when you
need to register multiple, independent cleanup callbacks from a single fixture.

### Scope

Scope controls how often a fixture is **(re)created**, i.e. how long its value is cached and
shared across tests:

| Scope | Created... |
|---|---|
| `function` (default) | Once per test function |
| `class` | Once per test class |
| `module` | Once per test file |
| `package` | Once per package (directory with `__init__.py`) |
| `session` | Once for the entire pytest run |

Use a wider scope for expensive setup you don't need to redo per test (e.g. spinning up a fake
database connection once per module) — see `../modern_pytest_course/app/database.py`'s
`FakeDatabase`, which simulates a slow startup (`time.sleep`) on purpose to demonstrate why
scope matters for test suite speed:

```python
@pytest.fixture(scope="module")
def tmp_file():
    ...
```

**Important gotcha:** a wider-scoped fixture is shared *by reference* across tests in that
scope. If your fixture returns a mutable object (like a list or the `FakeDatabase` above) and
one test mutates it, later tests in the same scope see that mutation. Either reset state
between tests (e.g. in an `autouse` function-scoped fixture) or keep mutable fixtures at
`function` scope.

### Fixture chaining/composition

A fixture can request other fixtures as parameters, so setup builds up in layers instead of one
fixture doing everything:

```python
@pytest.fixture
def store(tmp_path):
    path = tmp_path / "results.json"
    s = ResultStore(path)
    s.open()
    yield s
    s.close()

@pytest.fixture
def populated_store(store):        # depends on `store` above
    store.add_result("test_1", True)
    return store
```
(see `../test_types/tests/conftest.py`)

### Factory fixtures

Instead of returning one fixed value, a fixture can return a *function* the test calls multiple
times with different arguments — useful when a single fixed value isn't enough for a given
test (e.g. creating several temp files with different contents in one test).

### `autouse=True`

The fixture runs automatically for every test in its scope, without needing to be named as a
parameter — handy for logging, resetting global state, or enforcing environment invariants that
every test should have regardless of whether they "ask" for it.

### The `request` fixture

A built-in fixture giving access to metadata about the currently running test: its name
(`request.node.name`), its markers (`request.node.get_closest_marker(...)`), and — critically
for `indirect=True` parametrize — the parameter value via `request.param`.

### Built-in fixtures worth knowing

| Fixture | Purpose |
|---|---|
| `tmp_path` | A unique, real temporary directory (`pathlib.Path`) per test, auto-cleaned by pytest. |
| `tmp_path_factory` | Session-scoped factory for creating multiple temp directories (use when you need more than one, or need one shared across a wider scope). |
| `capsys` | Capture stdout/stderr printed during the test (`captured = capsys.readouterr()`). |
| `monkeypatch` | Safely patch attributes, dict items, env vars, or `sys.path` — every change is automatically undone after the test, even on failure. |
| `caplog` | Capture and assert on log records emitted via the `logging` module (`caplog.records`, `caplog.text`, `caplog.set_level(...)`). |

`monkeypatch` specifically supports: `setattr`, `delattr`, `setitem`, `delitem`, `setenv`,
`delenv`, and `chdir` — all automatically reverted, which is why it's preferred over manually
saving/restoring state yourself.

## 3b. Parametrized fixtures — `@pytest.fixture(params=...)`

`parametrize` (section 6) decorates one test with a list of inputs. A
parametrized fixture works the other way: the *fixture* holds the param
list, and every test that requests it runs once per value, automatically:

```python
@pytest.fixture(params=[3, 5, 10])
def sized_list(request):
    return list(range(request.param))

def test_len_matches_param(sized_list):
    assert len(sized_list) in (3, 5, 10)
```
(see `topics/test_16_fixture_params.py`)

Reach for this when several *different* tests all need to run against the
same set of inputs — writing `@pytest.mark.parametrize` on each of them
repeats the list; parametrizing the fixture once covers all of them.

## 4. `conftest.py` — sharing fixtures and hooks

Fixtures (and hooks) defined in `conftest.py` are automatically available to every test file in
that directory **and below** — no import needed; pytest discovers `conftest.py` files by
walking up from each test file. The repo root `../conftest.py` defines a `client` fixture and a
custom `--runslow` CLI option, consumed via `pytest_collection_modifyitems` (see below).
Sub-projects like `../test_types/tests/` and `../modern_pytest_course/` have their own
`conftest.py` for fixtures scoped to just that suite — a nested `conftest.py` can also
**override** a fixture of the same name defined higher up.

## 5. Markers

Markers tag tests with metadata, used for selection (`-m`) or special behavior:

```python
@pytest.mark.smoke        # custom marker (must be declared in pytest.ini's `markers`)
@pytest.mark.slow
@pytest.mark.skip(reason="not implemented yet")
@pytest.mark.skipif(sys.platform == "win32", reason="posix only")
@pytest.mark.xfail(reason="known bug, tracked in TICKET-123")
```

`xfail` marks a test as *expected* to fail — it still runs, but a failure is reported as `xfail`
(not a real failure) and an unexpected *pass* is reported as `XPASS`. Add `strict=True` to make
an unexpected pass count as a real failure (useful once you want to be notified the moment a
known bug gets fixed).

Custom markers must be registered in `pytest.ini` (see the root `../pytest.ini`'s `markers =`
section) or pytest emits an "unknown marker" warning. This repo defines `smoke` and `slow`, and
the root `conftest.py` auto-skips `slow` tests unless `--runslow` is passed — this is a
**pytest hook**, not a fixture, defined at the `conftest.py` module level:

```python
def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False,
                      help="run tests marked as slow")

def pytest_collection_modifyitems(config, items):
    # Runs once after collection, before execution — can inspect/modify the whole test list.
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```

## 6. `parametrize` — one test, many inputs

Runs the same test body once per set of parameters, instead of writing near-duplicate tests
that only differ in their literal values:

```python
@pytest.mark.parametrize("amount, item, results", [
    (3.0, "A1", {"item": "Espresso Shot", "change": 0.5}),
    (2.0, "B1", {"item": "Protein Bar", "change": 0.25}),
])
def test_vending_machine(vending_machine, amount, item, results):
    assert vending_machine.insert_coin(amount) == amount
    assert vending_machine.select_item(item) == results
```
(see `../vending_machine/test_vending_machine.py`)

- **`ids=[...]`** gives each parameter set a readable name in test output instead of an
  auto-generated index (e.g. `test_vending_machine[3.0-A1-results0]`), which otherwise gets
  unreadable fast for complex parameter values.
- **`pytest.param(..., id="...", marks=pytest.mark.xfail)`** lets you attach a custom id or a
  marker to just *one* specific parameter set, instead of the whole parametrize block.
- **`indirect=True`** routes the parameter value through a fixture first (the fixture receives
  it via `request.param` and can transform/build something from it) instead of passing the raw
  value straight to the test — useful when the "parameter" actually needs setup logic.
- Stacking `@pytest.mark.parametrize` twice on the same test multiplies the cases (full
  cross-product) — e.g. 3 values × 2 values = 6 test runs.

## 7. Testing exceptions with `pytest.raises`

```python
def test_invalid_amount_raises():
    with pytest.raises(ValueError, match="Amount inserted must be greater than zero."):
        vending_machine.insert_coin(-2)
```

Rules:
- Put **only** the line expected to raise inside the `with` block. Anything placed after it
  *inside* the block never runs once the exception fires, and any assertions that need to run
  regardless belong **after** the block, not inside it.
- `match=` is a **regex** search against `str(exception)`, not a literal substring match —
  escape special characters (`(`, `)`, `.`, `$`, `*`, ...) with `re.escape(...)`, or match a
  shorter, distinctive substring that has no regex metacharacters instead.
- To inspect the exception further, capture it with `as excinfo` and assert on
  `excinfo.value` **after** the `with` block (this is the only way to run more than one
  assertion about the exception, since the block exits as soon as the exception is raised):

```python
def test_invalid_config_details():
    with pytest.raises(ConfigurationError) as excinfo:
        load_config("broken.yaml")

    # These run because they are outside the with block
    assert "timeout" in str(excinfo.value)
    assert excinfo.value.field_name == "timeout"
    assert isinstance(excinfo.value.__cause__, KeyError)   # checks 'raise ... from e'
```

## 7b. `pytest.warns` — asserting a warning was raised

`warnings.warn(...)` doesn't stop execution, so `pytest.raises` can't catch
it — `pytest.warns` is the equivalent for warnings:

```python
def test_warns_on_zero_divisor():
    with pytest.warns(RuntimeWarning, match="zero"):
        risky_divide(10, 0)
```
(see `topics/test_17_pytest_warns.py`)

To assert the OPPOSITE — that a block raises no warning — wrap it in
`warnings.catch_warnings()` with `simplefilter("error")`, which turns any
warning into an exception for the duration of the block.

## 8. Mocking

`unittest.mock.Mock`/`MagicMock` create fake objects that record how they were called (call
count, arguments) and return canned values, so you can test code in isolation from slow,
flaky, or unavailable real dependencies (see `../test_types/mock_example.py` for a full example
against `GateController`):

```python
from unittest.mock import Mock

def test_authorized_tag_opens_gate():
    mock_db = Mock()
    mock_db.query.return_value = "found"     # canned return value
    controller = GateController(database=mock_db)
    assert controller.handle_tag("12345") == "GATE_OPEN"
    mock_db.query.assert_called_once_with("12345")  # verify HOW it was called
```

`Mock` vs `MagicMock`: `MagicMock` additionally implements Python's "magic methods"
(`__len__`, `__iter__`, etc.), so use it when the code under test relies on those protocols.

The **pytest-mock** plugin wraps `unittest.mock.patch` in a `mocker` fixture, so patches are
automatically undone after the test (tied to fixture teardown), without needing a `with
patch(...):` block or a `@patch` decorator that changes your function signature:

```python
def test_something(mocker):
    mocker.patch("module.function", return_value=42)
    mocker.patch.object(SomeClass, "method", side_effect=ValueError("boom"))
```

Compare **Fake vs Stub vs Mock vs Simulator** — see `../test_types/README.md` for the broader
distinction between these test-double styles, all demonstrated against the same
`GateController` example.

## 8b. `Mock(spec=...)` / `create_autospec` — catching typos in mocks

A plain `Mock()` accepts any attribute or method name — `fake.sedn(...)` (a
typo for `send`) silently returns another `Mock` instead of erroring, so a
test can pass while testing nothing real. `spec=` (on `Mock`) or
`create_autospec` restrict the mock to the real object's actual interface:

```python
fake = create_autospec(Sender, instance=True)
fake.send("a@example.com")   # matches the real signature - fine
fake.sedn("a@example.com")   # AttributeError - not a real Sender method
```
(see `topics/test_18_mock_spec_and_autospec.py`)

Prefer `spec`/`autospec` over a bare `Mock()` whenever the thing being
mocked is a real class already in the codebase — the cost is naming it,
the payoff is the mock breaking the moment the real interface changes.

## 8c. `pytest-cov` — measuring which lines your tests exercise

A passing suite doesn't mean every line ran; `pytest-cov` (built on the
`coverage` package) reports exactly which lines were and weren't executed:

```
python -m pytest topics/test_19_coverage_pytest_cov.py --cov=test_19_coverage_pytest_cov --cov-report=term-missing
```
(see `topics/test_19_coverage_pytest_cov.py`)

The `--cov` target is a module name, not a file path — for a directory
without `__init__.py` files (like this one) that's the bare module name
pytest imports it as, not a dotted package path. Other useful flags:
`--cov-report=html` (writes `htmlcov/index.html`) and `--cov-fail-under=90`
(non-zero exit if total coverage drops below a threshold — handy in CI).

## 9. `pytest.approx` — comparing floats

Floating point arithmetic is imprecise (e.g. `0.1 + 0.2 != 0.3` exactly); use `pytest.approx`
instead of `==` for float comparisons:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(expected, rel=1e-3)   # custom relative tolerance
```

## 10. Class-based tests

Grouping related tests in a class (no `__init__`, methods start with `test_`) shares structure
and lets you scope fixtures/markers to the whole group (e.g. a class-level
`@pytest.mark.parametrize` or a `@pytest.fixture(scope="class")` shared by all its methods):

```python
class TestVendingMachine:
    def test_initial_state(self, vending_machine):
        ...
```

## 11. Failure vs. Error

- **Failure** — an `assert` inside the test evaluated to `False`. The test logic ran to
  completion; the result just didn't match expectations.
- **Error** — an unexpected exception occurred *outside* of an assertion (e.g. a fixture
  raised during setup, or the test hit an unrelated bug/typo, like calling a method that
  doesn't exist). Pytest reports these separately (`E` vs `F` in the short summary) so you can
  tell "my code under test is wrong" apart from "my test/fixture setup is broken".

## 12. `pytest.skip` / `pytest.fail`

Imperative alternatives to the decorator markers, useful when the decision depends on a
runtime condition evaluated *inside* the test body (a decorator marker's condition, by
contrast, must be evaluate-able at collection time):

```python
def test_needs_network():
    if not has_network():
        pytest.skip("no network available")
    ...

def test_manual_fail():
    pytest.fail("not implemented")
```

## 13. Assert rewriting and plain scripts

Because assert rewriting is an *import-time* hook that pytest installs for test modules, a
function using `assert` will show rich diffs when imported and run *by pytest*, but only a bare
`AssertionError` when run as a plain script — this is why some files in this repo (e.g. those
under `../python_excrcises/`) are meant to be run directly with `python file.py`, while files
named `test_*.py` are meant to be run with `pytest`.

## Where to look next

| Topic | File |
|---|---|
| Everything above, in one file | [test_examples.py](test_examples.py) |
| Everything above, split one topic per file | [topics/](topics/README.md) |
| Fixture scopes in depth | [test_fixtures_examples.py](test_fixtures_examples.py) |
| General practice | [test_practice.py](test_practice.py) |
| Scope + config-reading patterns | [test_scope.py](test_scope.py) |
| Shared repo-wide fixtures/hooks | [../conftest.py](../conftest.py) |
| Repo-wide markers/config | [../pytest.ini](../pytest.ini) |
| Fakes/stubs/mocks/simulators compared | [../test_types/README.md](../test_types/README.md) |
