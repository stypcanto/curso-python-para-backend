from data import PRODUCTS


class ProductService:
    def get_product(
        self,
        product_id: int,
    ):
        return PRODUCTS[product_id]
