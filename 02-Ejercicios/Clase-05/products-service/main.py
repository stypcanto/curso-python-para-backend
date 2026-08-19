"""
Microservicio `products` — Clase 5, Python para Backend.

Versión mínima para practicar la idea de "microservicio independiente" antes de
construir el sistema completo de la Clase 6 (con API Gateway + varios servicios reales).
Expone solo lo que le corresponde a este servicio: el catálogo de productos.

Corresponde al microservicio `products` del diagrama de arquitectura de Clase-05.md
(el que en Clase 6 se conecta al API Gateway y en el diagrama de eventos consume
`order.created` desde Kafka para descontar stock).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="products-service",
    description="Microservicio independiente: catálogo de productos.",
    version="1.0.0",
)


class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int


# "Base de datos" en memoria — en Clase 6 esto pasa a ser su propia PostgreSQL
# (Database per Service), separada de la de `users` y `orders`.
PRODUCTS: list[Product] = [
    Product(id=1, name="Teclado mecánico", price=89.90, stock=15),
    Product(id=2, name="Mouse inalámbrico", price=29.90, stock=40),
    Product(id=3, name="Monitor 27''", price=249.00, stock=8),
]


@app.get("/")
def home():
    return {"service": "products", "status": "ok"}


@app.get("/products", response_model=list[Product])
def list_products():
    return PRODUCTS


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")
