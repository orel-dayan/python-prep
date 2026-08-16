import pytest
from app.cart import ShoppingCart


@pytest.fixture()
def cart():
    return ShoppingCart()


def test_cart_starts_empty(cart):
    assert cart.is_empty()
    
    
def test_add_item(cart):
    cart.add("Apple",1.00)
    
    assert cart.is_empty() is False
    assert cart.item_count() == 1 
    
    
def test_total_calculation(cart):
    cart.add("Apple",2.00)
    cart.add("Banana", 3.00, quantity=2)
    
    assert cart.total() == 8.00
    