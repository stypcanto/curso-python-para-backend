"""Ejercicio 5 — modelo de dominio rico ShoppingCart (solución)."""


class EmptyCartError(Exception):
    pass


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name: str, price: float):
        self.items.append({"name": name, "price": price})

    def checkout(self):
        if not self.items:
            raise EmptyCartError("El carrito está vacío")

        total = round(sum(item["price"] for item in self.items), 2)
        return {"items": self.items, "total": total}
