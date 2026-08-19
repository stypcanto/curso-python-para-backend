"""
Microservicio `products` — variante en Flask, Clase 5.

Mismo servicio que `products-service/main.py` (versión FastAPI), pero construido con
otro framework y consumiendo el catálogo desde una API pública externa (dummyjson.com)
en vez de una lista en memoria — para probar en carne propia la idea de "cada
microservicio puede usar el stack que más le convenga" (sección 2 de Clase-05.md).
"""

import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

DUMMYJSON_URL = "https://dummyjson.com"


@app.route("/")
def home():
    return "Hello, this is a Flask Microservice"


@app.route("/products", methods=["GET"])
def get_products():
    response = requests.get(f"{DUMMYJSON_URL}/products")
    if response.status_code != 200:
        return jsonify({"error": response.json().get("message", "error desconocido")}), response.status_code

    products = [
        {
            "id": product["id"],
            "title": product["title"],
            # No todos los productos de dummyjson.com traen "brand" (p. ej. categoría
            # "groceries") — .get() con default evita el KeyError que tira el .json()
            # directo si asumís que el campo siempre está.
            "brand": product.get("brand", "Sin marca"),
            "price": product["price"],
            "description": product["description"],
        }
        for product in response.json()["products"]
    ]
    return jsonify({"data": products}), 200 if products else 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
