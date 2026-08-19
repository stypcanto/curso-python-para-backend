"""
OrderService — versión refactorizada en servicios separados.

No estaba en la captura (esa mostraba solo UserService/ProductService/
InventoryService/NotificationService, cada uno en su propia clase); se agregó acá
para que el lab quede completo y ejecutable: alguien tiene que orquestar a los cuatro.

Notar qué NO cambió respecto a la versión monolítica (orders-monolitico/order_service.py):
la secuencia de pasos y las reglas de negocio son las mismas. Lo que cambió es que
`OrderService` ya no toca `USERS`/`PRODUCTS` directo — se los pide a cada servicio.

Segunda vuelta de tuerca: `notifications` ya se extrajo a su propio proceso
(../notifications-service/), así que acá se cambió `NotificationService` (clase
local, notification_service.py — se deja el archivo para comparar) por
`NotificationServiceClient` (llamada HTTP, notification_client.py). `users`,
`products` e `inventory` siguen locales todavía — la extracción es de a una pieza
por vez, no todo junto.
"""

from data import ORDERS
from inventory_service import InventoryService
from notification_client import NotificationServiceClient
from product_service import ProductService
from user_service import UserService


class OrderService:
    def __init__(self):
        self.users = UserService()
        self.products = ProductService()
        self.inventory = InventoryService()
        self.notifications = NotificationServiceClient()

    def create_order(self, user_id: int, product_id: int, quantity: int):
        user = self.users.get_user(user_id)
        product = self.products.get_product(product_id)

        # Antes: `if product["stock"] < quantity: raise ValueError(...)` vivía acá
        # mismo. Ahora esa regla es responsabilidad de InventoryService — OrderService
        # ya no sabe (ni le importa) cómo se valida o descuenta el stock.
        self.inventory.reserve(product_id, quantity)

        total = product["price"] * quantity

        order = {
            "user": user["name"],
            "product": product["name"],
            "quantity": quantity,
            "total": total,
        }
        ORDERS.append(order)

        self.notifications.send(
            email=user["email"],
            message=f"Tu pedido de {product['name']} fue confirmado.",
        )

        return order
