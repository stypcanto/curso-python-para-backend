"""Datos en memoria compartidos por los 4 servicios — mismo rol que en la versión
monolítica (orders-monolitico/order_service.py), separados acá para que cada archivo
de servicio los importe solo cuando le corresponde."""

USERS = {
    1: {"name": "Ana Torres", "email": "ana@example.com"},
    2: {"name": "Luis Paredes", "email": "luis@example.com"},
}

PRODUCTS = {
    1: {"name": "Teclado mecánico", "price": 89.90, "stock": 15},
    2: {"name": "Mouse inalámbrico", "price": 29.90, "stock": 40},
}

ORDERS = []
