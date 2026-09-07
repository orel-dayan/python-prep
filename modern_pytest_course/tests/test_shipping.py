import pytest
from app.shipping import calculate_shipping


def test_free_shipping_for_large_orders():
    assert calculate_shipping(100) == 0


def test_shipping_fee_for_small_orders():
    assert calculate_shipping(30) == 5


def test_negative_total_raises_value_error():
    with pytest.raises(ValueError):
        calculate_shipping(-10)


# @pytest.mark.skip(reason="This test is skipped because the shipping logic is not yet implemented for discounted orders.")
# @pytest.mark.xfail(
#     strict=True,
#     reason="This test is expected to fail because the shipping logic for discounted orders is not yet implemented.",
# )
def test_discounted_shipping():
    assert calculate_shipping(40) == 2
