import pytest

from vending_machine import InsufficientFundsError, OutOfStockError, VendingMachine


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
    assert vending_machine.inventory["A2"]["stock"] == 0
    

@pytest.mark.parametrize("amount, item, results", [
    (3.0, "A1", {"item": "Espresso Shot", "change": 0.5}),
    (2.0, "B1", {"item": "Protein Bar", "change": 0.25}),
])
def test_vending_machine(vending_machine, amount, item, results):
    assert vending_machine.insert_coin(amount) == amount
    assert vending_machine.select_item(item) == results


@pytest.mark.parametrize("amount, item, expected_error, error_message", [
    (2, "A1", InsufficientFundsError, "Need \\$0.50 more"),
    (-2, "A1", ValueError, "Amount inserted must be greater than zero."),
    (0, "A1", ValueError, "Amount inserted must be greater than zero."),
    (20, "A8", KeyError, "Invalid item code: A8"),
    (20, "A2", OutOfStockError, "'Matcha Latte' is out of stock."),
])
def test_vending_machine_errors(vending_machine, amount, item, expected_error, error_message):
    with pytest.raises(expected_error, match=error_message):
        vending_machine.insert_coin(amount)
        vending_machine.select_item(item)


def test_refund(vending_machine):
    assert vending_machine.refund() == 0
    vending_machine.insert_coin(3.0)
    vending_machine.insert_coin(2.0)
    vending_machine.insert_coin(2.0)
    with pytest.raises(ValueError):
        vending_machine.insert_coin(-8)
    assert vending_machine.refund() == 7

def test_stock_decrease(vending_machine):
    vending_machine.insert_coin(3.0)
    vending_machine.select_item("A1")
    assert vending_machine.inventory["A1"]["stock"] == 2

def test_stock_unchanged_after_insufficient_funds(vending_machine):
    vending_machine.insert_coin(1.0)
    with pytest.raises(InsufficientFundsError):
        vending_machine.select_item("A1")
    assert vending_machine.inventory["A1"]["stock"] == 3

def test_stock_unchanged_after_out_of_stock(vending_machine):
    vending_machine.inventory["A2"]["stock"] = 0
    vending_machine.insert_coin(20.0)
    with pytest.raises(OutOfStockError):
        vending_machine.select_item("A2")
    assert vending_machine.inventory["A2"]["stock"] == 0

@pytest.mark.parametrize("amount, item, expected_change", [
    (3.0, "A1", 0.5),
    (2.0, "B1", 0.25),
])

def test_purchase_returns_correct_change(vending_machine, amount, item, expected_change):
   vending_machine.insert_coin(amount)
   change = vending_machine.select_item(item)["change"]
   assert change == expected_change

@pytest.mark.parametrize("item", ["B1", "A1", "A2"])
def test_state_change(vending_machine ,item):
    stock = vending_machine.inventory[item]["stock"]
    price = vending_machine.inventory[item]["price"]

    for i in range(stock):
        vending_machine.insert_coin(2 * price)
        result = vending_machine.select_item(item)

        assert result["change"] == price
        assert vending_machine.inserted_money == 0
        assert vending_machine.inventory[item]["stock"] == stock - i - 1


    vending_machine.insert_coin(2 * price)
    with pytest.raises(OutOfStockError):
        vending_machine.select_item(item)
        

@pytest.mark.parametrize("code, amount, expected_item, expected_change", [
    ("A1", 3.0, "Espresso Shot", 0.5),
    ("B1", 2.0, "Protein Bar", 0.25),
])
def test_select_item_success(vending_machine, code, amount, expected_item, expected_change):
    vending_machine.insert_coin(amount)
    result = vending_machine.select_item(code)
    assert result["item"] == expected_item
    assert result["change"] == expected_change


# stock decrement and inserted money reset after successful purchase
@pytest.mark.parametrize("code, amount", [
    ("A1", 3.0),
    ("B1", 2.0),
])
def test_select_item_success_decrements_stock_and_resets_inserted_money(vending_machine, code, amount):
    initial_stock = vending_machine.inventory[code]["stock"]
    vending_machine.insert_coin(amount)
    vending_machine.select_item(code)
    assert vending_machine.inventory[code]["stock"] == initial_stock - 1
    assert vending_machine.inserted_money == 0.0
    
@pytest.mark.parametrize("code, results", [
    ("b1", {"item": "Protein Bar", "change": 0.25}),
    ("a1", {"item": "Espresso Shot", "change": 0.5}),
])
def test_lowercase_code_normalized(vending_machine, code, results):
    vending_machine.insert_coin(3.0 if code == "a1" else 2.0)
    assert vending_machine.select_item(code) == results
    
@pytest.mark.parametrize("coins, expected", [
    ([1.0, 0.5, 0.5], 2.0),
    ([2.0, 1.0], 3.0),
    ([2.0 , 2.0, 1.0], 5.0),
])
def test_insert_coin_accumulates(vending_machine, coins, expected):
    for coin in coins:
        total = vending_machine.insert_coin(coin)
    assert total == expected

