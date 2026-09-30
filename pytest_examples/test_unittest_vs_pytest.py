"""The same test written in unittest style and in pytest style.

Run: pytest test_unittest_vs_pytest.py -v
pytest can run unittest.TestCase classes without any change.
"""

import unittest

import pytest


# --- unittest style: class, self.assertX methods, setUp ---
class TestDiscount(unittest.TestCase):
    def setUp(self):
        self.price = 100

    def test_ten_percent(self):
        self.assertEqual(self.price * 0.9, 90)

    def test_twenty_percent(self):
        self.assertEqual(self.price * 0.8, 80)


# --- pytest style: plain functions, plain assert, fixture, parametrize ---
@pytest.fixture
def base_price():
    return 100


@pytest.mark.parametrize("percent, expected", [(10, 90), (20, 80)], ids=["10%", "20%"])
def test_discount(base_price, percent, expected):
    assert base_price * (1 - percent / 100) == expected
