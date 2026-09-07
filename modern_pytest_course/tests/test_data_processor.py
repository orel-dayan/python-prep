import pytest
from app.data_processor import fast_sum, slow_report


def test_fast_sum_basic():
    assert fast_sum([1, 2, 3]) == 6


def test_fast_sum_empty():
    assert fast_sum([]) == 0


def test_fast_sum_negative_numbers():
    assert fast_sum([-1, -2, -3]) == -6


@pytest.mark.slow
def test_slow_report():
    result = slow_report([10, 20, 30])
    assert result["count"] == 3
    assert result["sum"] == 60
    assert result["mean"] == 20.0
