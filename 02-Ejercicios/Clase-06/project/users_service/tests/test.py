from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_user():
    response = client.post("/api/v1/users", json={
        "name": "Ana Torres",
        "email": "ana@empresa.com"
    })

    assert response.status_code == 201

    data = response.json()
    assert data["name"] =="Ana Torres"