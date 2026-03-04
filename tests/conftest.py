import os
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

TEST_DB_FILE = Path("test_todo.db")
os.environ["DATABASE_URL"] = "sqlite:///./test_todo.db"
os.environ["DEBUG"] = "true"
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import models.todo  # noqa: F401
import models.user  # noqa: F401
from core.dependencies import get_db as core_get_db
from db.base import Base
from db.session import SessionLocal, engine
from main import app
from routers.auth import get_db as auth_get_db
from routers.todo import get_db as todo_get_db


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_dependencies():
    app.dependency_overrides[core_get_db] = override_get_db
    app.dependency_overrides[auth_get_db] = override_get_db
    app.dependency_overrides[todo_get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    engine.dispose()
    if TEST_DB_FILE.exists():
        TEST_DB_FILE.unlink()


@pytest.fixture(autouse=True)
def reset_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
