from data import PRODUCTS


class InventoryService:
    def reserve(
        self,
        product_id: int,
        quantity: int,
    ):
        product = PRODUCTS[product_id]

        if product["stock"] < quantity:
            raise ValueError(
                "Stock insuficiente"
            )

        product["stock"] -= quantity
