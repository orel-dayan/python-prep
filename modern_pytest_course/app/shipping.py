def calculate_shipping(total):
    if total >= 50:
        return 0  # Free shipping for orders $50 or more
    return 5  # Flat shipping rate for orders under $50