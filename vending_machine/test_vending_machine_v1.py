import pytest
from vending_machine_v1 import InsufficientFundsError, OutOfStockError, VendingMachine


@pytest.fixture
def vending_machine():
    return VendingMachine()


@pytest.mark.smoke
def test_smoke_basic_flow(vending_machine):
    """Insert enough money and buy an in-stock item without crashing."""
    vending_machine.insert_coin(2.0)
    result = vending_machine.select_item("B1")
    assert result == {"item": "Protein Bar", "change": 0.25}


def test_initial_state(vending_machine):
    assert vending_machine.inserted_money == 0
    assert set(vending_machine.inventory.keys()) == {"A1", "A2", "B1"}
    assert vending_machine.get_stock("A2") == 0


# ---------- getters ----------

@pytest.mark.parametrize("code, expected_stock", [
    ("A1", 3),
    ("a1", 3),
    ("A2", 0),
    ("B1", 5),
])
def test_get_stock(vending_machine, code, expected_stock):
    assert vending_machine.get_stock(code) == expected_stock


@pytest.mark.parametrize("code, expected_price", [
    ("A1", 2.50),
    ("A2", 4.00),
    ("b1", 1.75),
])
def test_get_price(vending_machine, code, expected_price):
    assert vending_machine.get_price(code) == expected_price


@pytest.mark.parametrize("getter", ["get_stock", "get_price"])
def test_getters_invalid_code(vending_machine, getter):
    with pytest.raises(KeyError, match="Invalid item code: Z9"):
        getattr(vending_machine, getter)("Z9")


# ---------- insert_coin ----------

@pytest.mark.parametrize("coins, expected", [
    ([1.0, 0.5, 0.5], 2.0),
    ([2.0, 1.0], 3.0),
    ([2.0, 2.0, 1.0], 5.0),
])
def test_insert_coin_accumulates(vending_machine, coins, expected):
    for coin in coins:
        total = vending_machine.insert_coin(coin)
    assert total == expected


# ---------- successful purchase ----------

@pytest.mark.parametrize("amount, item, results", [
    (3.0, "A1", {"item": "Espresso Shot", "change": 0.5}),
    (2.0, "B1", {"item": "Protein Bar", "change": 0.25}),
])
def test_vending_machine(vending_machine, amount, item, results):
    assert vending_machine.insert_coin(amount) == amount
    assert vending_machine.select_item(item) == results


@pytest.mark.parametrize("code, results", [
    ("b1", {"item": "Protein Bar", "change": 0.25}),
    ("a1", {"item": "Espresso Shot", "change": 0.5}),
])
def test_lowercase_code_normalized(vending_machine, code, results):
    vending_machine.insert_coin(3.0 if code == "a1" else 2.0)
    assert vending_machine.select_item(code) == results


@pytest.mark.parametrize("code, amount", [
    ("A1", 3.0),
    ("B1", 2.0),
])
def test_purchase_decrements_stock_and_resets_money(vending_machine, code, amount):
    initial_stock = vending_machine.get_stock(code)
    vending_machine.insert_coin(amount)
    vending_machine.select_item(code)
    assert vending_machine.get_stock(code) == initial_stock - 1
    assert vending_machine.inserted_money == 0.0


# ---------- errors ----------

@pytest.mark.parametrize("amount, item, expected_error, error_message", [
    (2, "A1", InsufficientFundsError, r"Need \$0.50 more"),
    (-2, "A1", ValueError, "Amount inserted must be greater than zero."),
    (0, "A1", ValueError, "Amount inserted must be greater than zero."),
    (20, "A8", KeyError, "Invalid item code: A8"),
    (20, "A2", OutOfStockError, "'Matcha Latte' is out of stock."),
])
def test_vending_machine_errors(vending_machine, amount, item, expected_error, error_message):
    with pytest.raises(expected_error, match=error_message):
        vending_machine.insert_coin(amount)
        vending_machine.select_item(item)


def test_stock_unchanged_after_insufficient_funds(vending_machine):
    vending_machine.insert_coin(1.0)
    with pytest.raises(InsufficientFundsError):
        vending_machine.select_item("A1")
    assert vending_machine.get_stock("A1") == 3


def test_stock_unchanged_after_out_of_stock(vending_machine):
    vending_machine.insert_coin(20.0)
    with pytest.raises(OutOfStockError):
        vending_machine.select_item("A2")
    assert vending_machine.get_stock("A2") == 0


# ---------- full lifecycle ----------

@pytest.mark.parametrize("item", ["B1", "A1", "A2"])
def test_state_change(vending_machine, item):
    stock = vending_machine.get_stock(item)
    price = vending_machine.get_price(item)

    for i in range(stock):
        vending_machine.insert_coin(2 * price)
        result = vending_machine.select_item(item)

        assert result["change"] == price
        assert vending_machine.inserted_money == 0
        assert vending_machine.get_stock(item) == stock - i - 1

    vending_machine.insert_coin(2 * price)
    with pytest.raises(OutOfStockError):
        vending_machine.select_item(item)


# ---------- refund ----------

def test_refund(vending_machine):
    assert vending_machine.refund() == 0
    vending_machine.insert_coin(3.0)
    vending_machine.insert_coin(2.0)
    vending_machine.insert_coin(2.0)
    with pytest.raises(ValueError):
        vending_machine.insert_coin(-8)
    assert vending_machine.refund() == 7
    assert vending_machine.inserted_money == 0.0


def test_refund_after_purchase_returns_zero(vending_machine):
    vending_machine.insert_coin(3.0)
    vending_machine.select_item("A1")
    assert vending_machine.refund() == 0.0
    
    
def test_validate_purchase_returns_item(vending_machine):
    vending_machine.insert_coin(3.0)
    item = vending_machine.validate_purchase("A1")
    assert item.name == "Espresso Shot"


def test_validate_purchase_does_not_change_state(vending_machine):
    vending_machine.insert_coin(3.0)
    vending_machine.validate_purchase("A1")
    assert vending_machine.get_stock("A1") == 3
    assert vending_machine.inserted_money == 3.0