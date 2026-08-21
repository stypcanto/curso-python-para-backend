from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas import (
    ProductCreate,
    ProductResponse,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

products: list[dict] = []


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
)
def create_product(
    data: ProductCreate,
):
    product = {
        "id": len(products) + 1,
        **data.model_dump(),
    }

    products.append(product)

    return product

##Añadir un endpoint para filtrar  productos tomando como base un stock minimo
##api/v1/products?minimum_stock=10

## "?"" es opcional

@router.get(
    "",
    response_model=list[ProductResponse],
    summary="Listar producto",
)

def list_products(
    minimum_stock: int | None = None,  # query param opcional: /products?minimum_stock=10
):
    # Sin filtro (no vino en la URL) -> se comporta como antes, devuelve todo
    if minimum_stock is None:
        return products

    # Con filtro -> arma una lista nueva solo con los productos que
    # tengan stock igual o mayor al mínimo pedido
    return [product  for product in products  if product["stock"] >= minimum_stock  ]


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto filtrado",
)

def get_product(
    product_id: int,
):
    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado",
    )
