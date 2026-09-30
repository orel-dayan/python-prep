import pytest

# PATTERN 1: Single parameter
@pytest.mark.parametrize("number", [1, 2, 3, 100])
def test_double(number):
    assert number * 2 == number + number

# PATTERN 2: Multiple parameters with ids
@pytest.mark.parametrize(
    "a, b, expected",
    [(2, 3, 5), (-1, 1, 0), (0, 5, 5), (1000000, 2000000, 3000000)],
    ids=["positive", "negative", "zero", "large"],
)
def test_add(a, b, expected):
    assert a + b == expected

# PATTERN 3: Stacked decorators — Cartesian product
@pytest.mark.parametrize("x", [0, 10])
@pytest.mark.parametrize("y", [0, 1, 2])
def test_multiply(x, y):
    assert x * y == x * y

# PATTERN 4: Parametrize with fixtures
@pytest.fixture
def base_price():
    return 100

@pytest.mark.parametrize("discount, expected", [(10, 90), (20, 80), (50, 50)])
def test_apply_discount(base_price, discount, expected):
    discounted = base_price * (1 - discount / 100)
    assert discounted == expected

# PATTERN 5: Testing exceptions with parametrize
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
        dividend / divisor