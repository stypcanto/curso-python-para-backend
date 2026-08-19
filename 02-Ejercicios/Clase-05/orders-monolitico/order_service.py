"""
OrderService — versión "monolítica" (acceso directo a USERS/PRODUCTS).

Esta es la versión que se muestra en la nota de Clase-05.md como ejemplo de qué NO
hacer si `OrderService` fuera parte de un microservicio `orders` real: toca directo
los datos de `users` y `products` en vez de pedírselos por su API. Existe para
poder correrla y comparar contra la versión corregida (orders-service/).

Datos en memoria (USERS/PRODUCTS/ORDERS) agregados solo para poder ejecutar y
verificar el método — no estaban en la captura original.
"""

USERS = {
    1: {"name": "Ana Torres", "email": "ana@example.com"},
    2: {"name": "Luis Paredes", "email": "luis@example.com"},
}

PRODUCTS = {
    1: {"name": "Teclado mecánico", "price": 89.90, "stock": 15},
    2: {"name": "Mouse inalámbrico", "price": 29.90, "stock": 40},
}

ORDERS = []


class OrderService:

    def create_order(self, user_id: int, product_id: int, quantity: int):
        # Usuarios
        user = USERS[user_id]

        # Productos
        product = PRODUCTS[product_id]

        # Inventario
        if product["stock"] < quantity:
            raise ValueError(
                "Stock insuficiente"
            )

        product["stock"] -= quantity

        # Pedidos
        total = (
            product["price"]
            * quantity
        )

        order = {
            "user": user["name"],
            "product": product["name"],
            "quantity": quantity,
            "total": total,
        }

        ORDERS.append(order)

        # Notificación
        print(
            f"Correo enviado a "
            f"{user['email']}"
        )

        return order
