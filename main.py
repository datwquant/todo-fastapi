from fastapi import FastAPI
from core.config import settings
from db.base import Base
from db.session import engine

# Import models để SQLAlchemy nhận diện bảng
import models.todo
import models.user

from routers import auth
from routers import todo

# Tạo app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Tạo bảng DB
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(todo.router)


@app.get("/health")
def health():
    return {"status": "ok"}