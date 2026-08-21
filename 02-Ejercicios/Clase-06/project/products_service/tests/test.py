from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_product():
    response = client.post("/api/v1/products", json={
        "name": "Teclado mecánico",
        "price": 49.99,
        "stock": 10,
    })

    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Teclado mecánico"


def test_list_products_filter_by_minimum_stock():
    client.post("/api/v1/products", json={
        "name": "Mouse",
        "price": 15.00,
        "stock": 5,
    })

    response = client.get("/api/v1/products", params={"minimum_stock": 10})

    assert response.status_code == 200
    for product in response.json():
        assert product["stock"] >= 10


def test_get_product_not_found():
    response = client.get("/api/v1/products/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"
