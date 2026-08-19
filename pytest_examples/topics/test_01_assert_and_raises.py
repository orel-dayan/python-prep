"""
Topic: plain `assert` + `pytest.raises`

Pytest rewrites `assert` at import time, so a failing assertion shows a full
diff of both sides instead of a bare AssertionError. `pytest.raises` is how
you assert that a specific exception (and optionally a message) was raised.

Run:
    python -m pytest pytest_examples/topics/test_01_assert_and_raises.py -v

Example run:
    2 tests should PASS. Try changing `add(2, 3) == 5` to `== 6` to see
    pytest's rich assertion diff on failure.
"""
import pytest


def add(a, b):
    return a + b


def div(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b


def test_add_basic():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_div_by_zero():
    # Only the raising line goes inside the `with` block.
    with pytest.raises(ValueError, match="division by zero"):
        div(1, 0)
