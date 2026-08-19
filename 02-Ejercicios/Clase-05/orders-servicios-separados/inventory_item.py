"""
InventoryItem — modelo de dominio "rico" (rich domain model) para el stock, en vez de
la versión "anémica" de inventory_service.py (una clase con un método que opera sobre
un dict PRODUCTS externo).

Acá el stock deja de ser un dict que cualquiera puede tocar (`product["stock"] -=
quantity`) y pasa a ser un atributo PRIVADO de su propio objeto, que solo se puede
modificar a través de un método que protege el invariante ("nunca reservar más de lo
que hay"). Es el mismo concepto de "Invariante" del glosario de la sección 3, ahora en
código real.
"""


class InsufficientStockError(Exception):
    pass


class InventoryItem:
    def __init__(
        self,
        sku: str,
        available_stock: int,
    ):
        self.sku = sku
        self.available_stock = (
            available_stock
        )

    def reserve(
        self,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError(
                "La cantidad debe "
                "ser positiva"
            )

        if quantity > self.available_stock:
            raise InsufficientStockError(
                f"Stock disponible: "
                f"{self.available_stock}"
            )

        self.available_stock -= quantity
