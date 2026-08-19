"""
Topic: `pytest.approx` - comparing floats safely

Floating point arithmetic is imprecise (e.g. 0.1 + 0.2 != 0.3 exactly);
`pytest.approx` compares within a tolerance instead of using `==` directly.

Run:
    python -m pytest pytest_examples/topics/test_12_approx.py -v

Example run:
    1 test should PASS.
"""
import pytest


def test_float_comparison():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 100 == pytest.approx(101, rel=0.02)
