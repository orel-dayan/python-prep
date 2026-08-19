"""
Topic: `parametrize` with readable ids

Runs the same test body once per set of parameters, instead of writing
near-duplicate tests. `ids=` gives each case a readable name in the test
output instead of an auto-generated index.

Run:
    python -m pytest pytest_examples/topics/test_07_parametrize.py -v

Example run:
    3 tests should PASS, shown as test_is_positive[positive],
    test_is_positive[negative], test_is_positive[zero].
"""
import pytest


def is_positive(num):
    return num > 0


@pytest.mark.parametrize("num, expected", [
    (2, True),
    (-4, False),
    (0, False),
], ids=["positive", "negative", "zero"])
def test_is_positive(num, expected):
    assert is_positive(num) == expected
