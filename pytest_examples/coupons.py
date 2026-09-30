"""Code under test for test_coupons.py."""


def apply_coupon(price: float, coupon: str) -> float:
    if coupon == "SAVE20":
        return price * 0.8
    if coupon == "FREESHIP":
        return price  # Shipping logic would go here
    return price
