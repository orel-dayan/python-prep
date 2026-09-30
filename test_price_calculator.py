# io.thecodeforge.pytest
# test_price_calculator.py
# Run with: pytest test_price_calculator.py -v

def apply_discount(original_price: float, discount_percent: float) -> float:
    if not (0 <= discount_percent <= 100):
        raise ValueError(f"Discount must be between 0 and 100, got {discount_percent}")
    discount_amount = original_price * (discount_percent / 100)
    return round(original_price - discount_amount, 2)

def test_apply_discount_returns_correct_price():
    discounted = apply_discount(original_price=200.00, discount_percent=10)
    assert discounted == 180.00

def test_apply_discount_with_zero_percent_returns_original():
    discounted = apply_discount(original_price=99.99, discount_percent=0)
    assert discounted == 99.99

def test_apply_discount_with_full_discount_returns_zero():
    discounted = apply_discount(original_price=50.00, discount_percent=100)
    assert discounted == 0.00

def test_apply_discount_raises_for_negative_discount():
    import pytest
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        apply_discount(original_price=100.00, discount_percent=-5)