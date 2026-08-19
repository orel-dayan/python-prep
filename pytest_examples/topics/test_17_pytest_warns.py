"""
Topic: `pytest.warns` — the `pytest.raises` of warnings

`warnings.warn(...)` doesn't stop execution, so `pytest.raises` can't catch
it. `pytest.warns` asserts a warning of the given category was emitted
(optionally matching a message regex), the same way `pytest.raises` asserts
an exception was raised.

Run:
    python -m pytest pytest_examples/topics/test_17_pytest_warns.py -v

Example run:
    2 tests should PASS.
"""
import warnings

import pytest


def risky_divide(a: float, b: float) -> float:
    if b == 0:
        warnings.warn("b is zero, returning 0 instead of dividing", RuntimeWarning)
        return 0
    return a / b


def test_warns_on_zero_divisor():
    with pytest.warns(RuntimeWarning, match="zero"):
        risky_divide(10, 0)


def test_no_warning_on_normal_input():
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # any warning here becomes a test failure
        assert risky_divide(10, 2) == 5
