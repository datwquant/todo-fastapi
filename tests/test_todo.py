def register_and_login(client):
    email = "level7@example.com"
    password = "123456"

    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password}
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_todo_success_200(client):
    headers = register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "Learn FastAPI"},
        headers=headers
    )
    assert response.status_code == 200


def test_create_todo_validation_fail_422(client):
    headers = register_and_login(client)
    response = client.post(
        "/api/v1/todos",
        json={"title": "ab"},
        headers=headers
    )
    assert response.status_code == 422


def test_get_todo_not_found_404(client):
    headers = register_and_login(client)
    response = client.get("/api/v1/todos/999999", headers=headers)
    assert response.status_code == 404


def test_get_todos_auth_fail_401(client):
    response = client.get("/api/v1/todos")
    assert response.status_code == 401
