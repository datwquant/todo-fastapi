from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.todo import TodoCreate, TodoListResponse
from repositories.todo_repository import TodoRepository
from db.session import SessionLocal

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


# =========================
# Dependency: tạo DB session cho mỗi request
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE
# =========================
@router.post("")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    repo = TodoRepository(db)
    return repo.create(todo)


# =========================
# GET LIST (pagination thật từ DB)
# =========================
@router.get("", response_model=TodoListResponse)
def get_todos(limit: int = 10, offset: int = 0,
              db: Session = Depends(get_db)):
    repo = TodoRepository(db)

    items = repo.get_all(limit, offset)
    total = repo.count()

    return TodoListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )


# =========================
# GET BY ID
# =========================
@router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    repo = TodoRepository(db)
    todo = repo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# =========================
# DELETE
# =========================
@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    repo = TodoRepository(db)
    todo = repo.delete(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted"}


# =========================
# PATCH (update 1 phần)
# =========================
@router.patch("/{todo_id}")
def patch_todo(todo_id: int, data: dict,
               db: Session = Depends(get_db)):
    repo = TodoRepository(db)
    todo = repo.patch(todo_id, data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# =========================
# COMPLETE endpoint
# =========================
@router.post("/{todo_id}/complete")
def complete(todo_id: int, db: Session = Depends(get_db)):
    repo = TodoRepository(db)
    todo = repo.patch(todo_id, {"is_done": True})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo