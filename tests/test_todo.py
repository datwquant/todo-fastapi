from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_todo():
    response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo", "is_done": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert "id" in data
    assert "created_at" in data


def test_validation_fail():
    response = client.post(
        "/api/v1/todos",
        json={"title": "ab"}  # < 3 ký tự
    )
    assert response.status_code == 422


def test_get_all():
    response = client.get("/api/v1/todos")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_not_found():
    response = client.get("/api/v1/todos/999")
    assert response.status_code == 404


def test_filter():
    client.post("/api/v1/todos", json={"title": "Done task", "is_done": True})
    response = client.get("/api/v1/todos?is_done=true")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert item["is_done"] is True


def test_pagination():
    response = client.get("/api/v1/todos?limit=1&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 1