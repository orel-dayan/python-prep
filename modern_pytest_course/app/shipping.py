FREE_SHIPPING_THRESHOLD = 50
STANDARD_SHIPPING_FEE = 5
SHIPPING_DISCOUNT_THRESHOLD = 40


def calculate_shipping(total):
    if total < 0:
        raise ValueError("Total amount cannot be negative.")

    if total >= FREE_SHIPPING_THRESHOLD:
        return 0

    elif total >= SHIPPING_DISCOUNT_THRESHOLD:
        return 2  # discounted shipping fee for orders between $40 and $49.99

    return STANDARD_SHIPPING_FEE
