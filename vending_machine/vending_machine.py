# vending_machine.py


class OutOfStockError(Exception):
    """Raised when trying to purchase an item with 0 quantity."""


class InsufficientFundsError(Exception):
    """Raised when inserted money is less than the item price."""


class VendingMachine:
    def __init__(self):
        # Format: "code": {"name": str, "price": float, "stock": int}
        self.inventory = {
            "A1": {"name": "Espresso Shot", "price": 2.50, "stock": 3},
            "A2": {"name": "Matcha Latte", "price": 4.00, "stock": 0},  # Out of stock!
            "B1": {"name": "Protein Bar", "price": 1.75, "stock": 5},
        }
        self.inserted_money = 0.0

    def insert_coin(self, amount: float) -> float:
        """Accepts positive coin/bill amounts and updates inserted_money."""
        if amount <= 0:
            raise ValueError("Amount inserted must be greater than zero.")
        self.inserted_money += amount
        return round(self.inserted_money, 2)

    def select_item(self, code: str) -> dict:
        """Processes purchase for an item code.

        Returns a dictionary with 'item' name and 'change' owed.
        """
        code = code.upper()

        if code not in self.inventory:
            raise KeyError(f"Invalid item code: {code}")

        item = self.inventory[code]

        if item["stock"] <= 0:
            raise OutOfStockError(f"'{item['name']}' is out of stock.")

        if self.inserted_money < item["price"]:
            missing = item["price"] - self.inserted_money
            raise InsufficientFundsError(
                f"Need ${missing:.2f} more to purchase '{item['name']}'."
            )

        # Successful transaction
        item["stock"] -= 1
        change = round(self.inserted_money - item["price"], 2)
        self.inserted_money = 0.0  # Reset inserted money

        return {"item": item["name"], "change": change}

    def refund(self) -> float:
        """Cancels transaction and returns all inserted money."""
        amount = self.inserted_money
        self.inserted_money = 0.0
        return round(amount, 2)
