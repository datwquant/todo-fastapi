from fastapi import FastAPI
from routers.todo import router as todo_router
from core.config import settings
from db.base import Base
from db.session import engine
import models.todo


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(todo_router)

@app.get("/health")
def health():
    return {"status": "ok"}