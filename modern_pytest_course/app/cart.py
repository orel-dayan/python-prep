class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, name, price, quantity=1):
        self.items.append(
            {
                "name": name,
                "price": price,
                "quantity": quantity,
            }
        )

    def remove(self, name):
        self.items = [i for i in self.items if i["name"] != name]

    def total(self):
        return sum(i["price"] * i["quantity"] for i in self.items)

    def item_count(self):
        return sum(i["quantity"] for i in self.items)

    def is_empty(self):
        return len(self.items) == 0
