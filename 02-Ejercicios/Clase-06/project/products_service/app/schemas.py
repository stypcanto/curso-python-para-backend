from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=120,
    )

    price: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    stock: int = Field(
        default=0,
        ge=0,
    )


class ProductResponse(ProductCreate):
    id: int
