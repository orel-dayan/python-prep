"""Coverage gate demo.

Run: pytest test_coupons.py --cov=coupons --cov-report=term-missing --cov-fail-under=80
To see the gate fail: comment out the last two tests and run again.
"""

from coupons import apply_coupon


def test_save20_coupon():
    assert apply_coupon(100, "SAVE20") == 80.0


def test_freeship_coupon():
    assert apply_coupon(100, "FREESHIP") == 100


def test_unknown_coupon():
    assert apply_coupon(100, "NOPE") == 100
