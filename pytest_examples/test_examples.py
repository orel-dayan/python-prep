"""
Comprehensive pytest examples file.
Covers: assert, raises, fixtures (scope/chaining/factory/autouse),
request fixture, markers (smoke/slow/skip/skipif/xfail), parametrize
(with ids and indirect), mocking (unittest.mock and pytest-mock),
built-in fixtures (tmp_path/capsys/monkeypatch/caplog), approx,
pytest.skip/pytest.fail, class-based tests, failure vs error.

Run with: pytest -v -s
"""
import logging
import sys
import time
from unittest.mock import Mock, patch

import pytest


# ---------------------------------------------------------------------------
# Functions under test
# ---------------------------------------------------------------------------
def add(a, b):
    return a + b


def div(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b


def is_positive(num):
    return num > 0


def notify_user(email, sender):
    # "sender" is an injected dependency (e.g. an email service)
    return sender.send(email)


# ---------------------------------------------------------------------------
# 1. Basic assert test
# ---------------------------------------------------------------------------
def test_add_basic():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


# ---------------------------------------------------------------------------
# 2. Exception testing with pytest.raises
# ---------------------------------------------------------------------------
def test_div_by_zero():
    with pytest.raises(ValueError, match="division by zero"):
        div(1, 0)


# ---------------------------------------------------------------------------
# 3. Fixture - basic data fixture with setup/teardown (yield)
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_list():
    data = [1, 2, 3]       # setup
    yield data
    data.clear()            # teardown, runs after the test finishes


def test_list_length(sample_list):
    assert len(sample_list) == 3


# ---------------------------------------------------------------------------
# 4. Fixture scope (module scope: created once for this whole file)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def shared_config():
    print("\n[setup] creating config once for the whole module")
    return {"env": "test"}


def test_config_a(shared_config):
    assert shared_config["env"] == "test"


def test_config_b(shared_config):
    # Same object as in test_config_a - fixture only ran once
    assert shared_config["env"] == "test"


# ---------------------------------------------------------------------------
# 5. Fixture chaining - a fixture that depends on another fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def db_connection():
    return {"connected": True}


@pytest.fixture
def user_repo(db_connection):
    return {"db": db_connection, "users": ["orel"]}


def test_find_user(user_repo):
    assert "orel" in user_repo["users"]


# ---------------------------------------------------------------------------
# 6. Fixture factory - a fixture that returns a function
# ---------------------------------------------------------------------------
@pytest.fixture
def make_user():
    def _make_user(name="default", age=30):
        return {"name": name, "age": age}
    return _make_user


def test_user_creation(make_user):
    user = make_user(name="Orel")
    assert user["name"] == "Orel"


# ---------------------------------------------------------------------------
# 7. Autouse fixture - runs automatically for every test in this file
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def log_test_boundaries():
    print("\n[setup] starting test")
    yield
    print("[teardown] finished test")


# ---------------------------------------------------------------------------
# 8. request fixture - dynamic behavior based on the calling test
# ---------------------------------------------------------------------------
@pytest.fixture
def resource(request):
    print(f"Running: {request.node.name}")
    marker = request.node.get_closest_marker("slow")
    if marker:
        print("This is a slow test")
    yield "data"


def test_resource_fast(resource):
    assert resource == "data"


@pytest.mark.slow
def test_resource_slow(resource):
    assert resource == "data"


# ---------------------------------------------------------------------------
# 9. Markers: smoke, slow, skip, skipif, xfail
# ---------------------------------------------------------------------------
@pytest.mark.smoke
def test_add_smoke():
    assert add(1, 1) == 2


@pytest.mark.slow
def test_heavy_computation():
    time.sleep(0.1)  # simulates a slow operation
    assert add(2, 2) == 4


@pytest.mark.skip(reason="not implemented yet")
def test_future_feature():
    ...


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires Python 3.8+")
def test_conditional_skip():
    assert add(1, 2) == 3


@pytest.mark.xfail(reason="known bug - demonstrates a failing assertion")
def test_known_bug():
    assert add(1, 1) == 1


# ---------------------------------------------------------------------------
# 10. Parametrize, with readable ids
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("num, expected", [
    (2, True),
    (-4, False),
    (0, False),
], ids=["positive", "negative", "zero"])
def test_is_positive(num, expected):
    assert is_positive(num) == expected


# ---------------------------------------------------------------------------
# 11. Parametrize with indirect=True - value is passed through a fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def sized_list(request):
    size = request.param
    return list(range(size))


@pytest.mark.parametrize("sized_list", [3, 5, 10], indirect=True)
def test_sized_list(sized_list):
    assert len(sized_list) in (3, 5, 10)


# ---------------------------------------------------------------------------
# 12. Mocking with unittest.mock (Mock + patch)
# ---------------------------------------------------------------------------
def test_with_mock_object():
    fake_sender = Mock()
    fake_sender.send.return_value = True

    result = notify_user("test@example.com", fake_sender)

    assert result is True
    fake_sender.send.assert_called_once_with("test@example.com")


@patch("builtins.print")
def test_patch_builtin(mock_print):
    print("hello")
    mock_print.assert_called_once_with("hello")


# ---------------------------------------------------------------------------
# 13. Mocking with pytest-mock (the "mocker" fixture)
#     Requires: pip install pytest-mock
# ---------------------------------------------------------------------------
def test_with_mocker(mocker):
    mock_sender = mocker.Mock()
    mock_sender.send.return_value = True

    result = notify_user("test@example.com", mock_sender)

    assert result is True
    mock_sender.send.assert_called_once()


# ---------------------------------------------------------------------------
# 14. Built-in fixtures: tmp_path, capsys, monkeypatch, caplog
# ---------------------------------------------------------------------------
def test_tmp_path(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"


def test_capsys(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"


def test_monkeypatch(monkeypatch):
    import os
    monkeypatch.setenv("MY_VAR", "test_value")
    assert os.environ["MY_VAR"] == "test_value"


def test_caplog(caplog):
    with caplog.at_level(logging.INFO):
        logging.info("something happened")
    assert "something happened" in caplog.text


# ---------------------------------------------------------------------------
# 15. approx - comparing floats safely
# ---------------------------------------------------------------------------
def test_float_comparison():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 100 == pytest.approx(101, rel=0.02)


# ---------------------------------------------------------------------------
# 16. pytest.skip / pytest.fail called from inside a test body
# ---------------------------------------------------------------------------
def test_conditional_runtime_skip():
    feature_enabled = False
    if not feature_enabled:
        pytest.skip("feature not enabled in this environment")
    assert add(1, 1) == 2


def test_manual_fail():
    valid_state = True
    if not valid_state:
        pytest.fail("state was invalid")
    assert True


# ---------------------------------------------------------------------------
# 17. Class-based tests with setup_method / teardown_method
# ---------------------------------------------------------------------------
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def teardown_method(self):
        self.calc = None

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(5, 2) == 3


# ---------------------------------------------------------------------------
# 18. Failure (F) vs Error (E) - shown for reference, both pass here
# ---------------------------------------------------------------------------
def test_this_is_a_failure_example():
    # An assert that does not hold is reported as "F".
    # Flip to add(1, 1) == 3 to see a real failure.
    assert add(1, 1) == 2


def test_this_is_an_error_example():
    # An unexpected exception is reported as "E", not "F".
    # Uncomment the line below to see it in action:
    # result = 1 / 0
    assert True
