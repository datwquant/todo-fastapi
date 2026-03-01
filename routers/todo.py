from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.todo import TodoCreate, TodoListResponse
from repositories.todo_repository import TodoRepository
from db.session import SessionLocal
from core.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


# =========================
# DB session dependency
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
def create_todo(
    todo: TodoCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)
    return repo.create(todo, current_user.id)


# =========================
# GET LIST (chỉ lấy todo của user hiện tại)
# =========================
@router.get("", response_model=TodoListResponse)
def get_todos(
    limit: int = 10,
    offset: int = 0,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)

    items = repo.get_all(current_user.id, limit, offset)
    total = repo.count(current_user.id)

    return TodoListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )


# =========================
# GET BY ID (bảo mật owner)
# =========================
@router.get("/{todo_id}")
def get_todo(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)
    todo = repo.get_by_id(todo_id, current_user.id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


# =========================
# DELETE
# =========================
@router.delete("/{todo_id}")
def delete(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)
    todo = repo.delete(todo_id, current_user.id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Deleted"}


# =========================
# PATCH
# =========================
@router.patch("/{todo_id}")
def patch_todo(
    todo_id: int,
    data: dict,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)
    todo = repo.patch(todo_id, current_user.id, data)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


# =========================
# COMPLETE
# =========================
@router.post("/{todo_id}/complete")
def complete(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repo = TodoRepository(db)
    todo = repo.patch(todo_id, current_user.id, {"is_done": True})

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo