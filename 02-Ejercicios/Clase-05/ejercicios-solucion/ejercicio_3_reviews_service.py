"""Ejercicio 3 — microservicio `reviews` (solución)."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="reviews-service")


class Review(BaseModel):
    id: int
    product_id: int
    rating: int
    comment: str


REVIEWS: list[Review] = [
    Review(id=1, product_id=1, rating=5, comment="Excelente, muy cómodo."),
    Review(id=2, product_id=1, rating=4, comment="Bueno, pero ruidoso."),
    Review(id=3, product_id=2, rating=3, comment="Cumple, nada más."),
]


@app.get("/reviews", response_model=list[Review])
def list_reviews():
    return REVIEWS


@app.get("/reviews/{review_id}", response_model=Review)
def get_review(review_id: int):
    for review in REVIEWS:
        if review.id == review_id:
            return review
    raise HTTPException(status_code=404, detail="Reseña no encontrada")
