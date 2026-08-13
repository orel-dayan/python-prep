# vending machine version 1.0
from dataclasses import dataclass


class OutOfStockError(Exception):
    """Raised when trying to purchase an item with 0 quantity."""


class InsufficientFundsError(Exception):
    """Raised when inserted money is less than the item price."""


@dataclass
class Item:
    name: str
    price: float
    stock: int = 0


class VendingMachine:

    def __init__(self):
        self.inventory: dict[str, Item] = {
            "A1": Item(name="Espresso Shot", price=2.50, stock=3),
            "A2": Item(name="Matcha Latte", price=4.00),
            "B1": Item(name="Protein Bar", price=1.75, stock=5),
        }
        self.inserted_money: float = 0.0

    def _get_item(self, code: str) -> Item:
        """Helper method to retrieve an item by code."""
        code = code.upper()
        if code not in self.inventory:
            raise KeyError(f"Invalid item code: {code}")
        return self.inventory[code]

    def get_stock(self, code: str) -> int:
        """Returns the stock of the item corresponding to the given code."""
        return self._get_item(code).stock

    def get_price(self, code: str) -> float:
        """Returns the price of the item corresponding to the given code."""
        return self._get_item(code).price

    def validate_purchase(self, code: str) -> Item:
        """Validates the purchase and returns the item if it can be sold."""
        item = self._get_item(code)

        if item.stock <= 0:
            raise OutOfStockError(f"'{item.name}' is out of stock.")

        if self.inserted_money < item.price:
            needed = round(item.price - self.inserted_money, 2)
            raise InsufficientFundsError(f"Need ${needed:.2f} more")

        return item

    def insert_coin(self, amount: float) -> float:
        """Accepts positive coin/bill amounts and updates inserted_money."""
        if amount <= 0:
            raise ValueError("Amount inserted must be greater than zero.")
        self.inserted_money = round(self.inserted_money + amount, 2)
        return self.inserted_money

    def select_item(self, code: str) -> dict:
        """Processes purchase for an item code.

        Returns a dictionary with 'item' name and 'change' owed.
        """
        item = self.validate_purchase(code)

        change = round(self.inserted_money - item.price, 2)
        item.stock -= 1
        self.inserted_money = 0.0

        return {"item": item.name, "change": change}

    def refund(self) -> float:
        """Returns the inserted money and resets it to 0."""
        refunded_amount = self.inserted_money
        self.inserted_money = 0.0
        return round(refunded_amount, 2)
    