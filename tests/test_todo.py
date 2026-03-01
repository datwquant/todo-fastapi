from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_user_and_token():
    client.post("/api/v1/auth/register",
                json={"email": "t@test.com", "password": "123456"})

    res = client.post("/api/v1/auth/login",
                      json={"email": "t@test.com", "password": "123456"})

    return res.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_todo():
    token = create_user_and_token()

    response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo"},
        headers=auth_header(token)
    )

    assert response.status_code == 200