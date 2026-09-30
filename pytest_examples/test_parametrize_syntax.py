"""All the parametrize patterns in one file.

Run: pytest test_parametrize_syntax.py -v
"""

import pytest


# PATTERN 1: single parameter
@pytest.mark.parametrize("number", [1, 2, 3, 100])
def test_double(number):
    assert number * 2 == number + number


# PATTERN 2: multiple parameters with readable ids
@pytest.mark.parametrize(
    "a, b, expected",
    [(2, 3, 5), (-1, 1, 0), (0, 5, 5), (1_000_000, 2_000_000, 3_000_000)],
    ids=["positive", "negative", "zero", "large"],
)
def test_add(a, b, expected):
    assert a + b == expected


# PATTERN 3: stacked decorators give a Cartesian product (2 x 3 = 6 tests)
@pytest.mark.parametrize("x", [0, 10])
@pytest.mark.parametrize("y", [0, 1, 2])
def test_multiply_is_commutative(x, y):
    assert x * y == y * x


# PATTERN 4: parametrize together with a fixture
@pytest.fixture
def base_price():
    return 100


@pytest.mark.parametrize("discount, expected", [(10, 90), (20, 80), (50, 50)])
def test_apply_discount(base_price, discount, expected):
    assert base_price * (1 - discount / 100) == expected


# PATTERN 5: testing exceptions with several inputs
@pytest.mark.parametrize(
    "dividend, divisor, expected_exception, match_text",
    [
        (10, 0, ZeroDivisionError, "division by zero"),
        (10, "a", TypeError, "unsupported operand type"),
    ],
    ids=["divide_by_zero", "type_error"],
)
def test_divide_exceptions(dividend, divisor, expected_exception, match_text):
    with pytest.raises(expected_exception, match=match_text):
        _ = dividend / divisor
