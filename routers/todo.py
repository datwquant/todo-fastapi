from fastapi import APIRouter, HTTPException
from schemas.todo import TodoCreate, Todo
from services.todo_service import TodoService
from repositories.todo_repository import TodoRepository
from schemas.todo import TodoListResponse

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])

repo = TodoRepository()
service = TodoService(repo)


@router.post("", response_model=Todo)
def create_todo(todo: TodoCreate):
    return repo.create(todo)


@router.get("", response_model=TodoListResponse)
def get_todos(is_done: bool | None = None,
              q: str | None = None,
              sort: str | None = None,
              limit: int = 10,
              offset: int = 0):
    return service.get_todos(is_done, q, sort, limit, offset)


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = repo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}")
def delete(todo_id: int):
    todo = repo.delete(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted"}