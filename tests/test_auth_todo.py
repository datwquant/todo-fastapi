from fastapi.testclient import TestClient
from main import app
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from db.base import Base

client = TestClient(app)


def register_user(email, password):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password}
    )


def login_user(email, password):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    return response.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# =========================
# TEST REGISTER + LOGIN
# =========================
def test_register_and_login():
    register_user("a@test.com", "123456")

    token = login_user("a@test.com", "123456")
    assert token is not None


# =========================
# TEST AUTH FAIL
# =========================
def test_login_fail():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@test.com", "password": "123"}
    )
    assert response.status_code == 401


# =========================
# TEST USER ISOLATION
# =========================
def test_user_isolation():
    # User A
    register_user("userA@test.com", "123456")
    tokenA = login_user("userA@test.com", "123456")

    # User B
    register_user("userB@test.com", "123456")
    tokenB = login_user("userB@test.com", "123456")

    # User A tạo todo
    response = client.post(
        "/api/v1/todos",
        json={"title": "Todo A"},
        headers=auth_headers(tokenA)
    )
    assert response.status_code == 200
    todo_id = response.json()["id"]

    # User B không thấy todo của A
    response = client.get(
        "/api/v1/todos",
        headers=auth_headers(tokenB)
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0

    # User B không xóa được todo của A
    response = client.delete(
        f"/api/v1/todos/{todo_id}",
        headers=auth_headers(tokenB)
    )
    assert response.status_code == 404


# =========================
# TEST PATCH + COMPLETE
# =========================
def test_patch_and_complete():
    register_user("patch@test.com", "123456")
    token = login_user("patch@test.com", "123456")

    # tạo todo
    response = client.post(
        "/api/v1/todos",
        json={"title": "Patch me"},
        headers=auth_headers(token)
    )
    todo_id = response.json()["id"]

    # patch
    response = client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"is_done": True},
        headers=auth_headers(token)
    )
    assert response.status_code == 200
    assert response.json()["is_done"] is True

    # complete endpoint
    response = client.post(
        f"/api/v1/todos/{todo_id}/complete",
        headers=auth_headers(token)
    )
    assert response.status_code == 200
    assert response.json()["is_done"] is True

    from datetime import datetime, timedelta


def test_get_today(client):
    # ===== Register =====
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "today@example.com",
            "password": "123456"
        }
    )

    # ===== Login =====
    res = client.post(
        "/api/v1/auth/login",
        data={
            "username": "today@example.com",
            "password": "123456"
        }
    )

    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ===== Create TODO hôm nay =====
    today = datetime.utcnow().replace(hour=10, minute=0, second=0)

    client.post(
        "/api/v1/todos",
        json={
            "title": "Task today",
            "description": "Must show in today",
            "due_date": today.isoformat()
        },
        headers=headers
    )

    # ===== Create TODO ngày mai =====
    tomorrow = today + timedelta(days=1)

    client.post(
        "/api/v1/todos",
        json={
            "title": "Task tomorrow",
            "description": "Must NOT show in today",
            "due_date": tomorrow.isoformat()
        },
        headers=headers
    )

    # ===== Call /today =====
    res = client.get(
        "/api/v1/todos/today",
        headers=headers
    )

    assert res.status_code == 200

    data = res.json()

    assert len(data) == 1
    assert data[0]["title"] == "Task today"