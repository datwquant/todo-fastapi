from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

app = FastAPI()

# Model dùng để CREATE / UPDATE
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False

# Model dùng để RESPONSE
class Todo(TodoCreate):
    id: int
    created_at: datetime

class TodoListResponse(BaseModel):
    items: List[Todo]
    total: int
    limit: int
    offset: int

# data trong ram
todos: List[Todo] = []
current_id = 1

# CREATE (POST /todos)
@app.post("/todos", response_model = Todo)
def create_todo(todo: TodoCreate):
    global current_id
    # new_todo = Todo(id=current_id, **todo.dict())
    new_todo = Todo(
    id=current_id,
    created_at=datetime.utcnow(),
    **todo.dict()
    )
    todos.append(new_todo)
    current_id += 1
    return new_todo

# READ LIST (GET /todos)
@app.get("/todos", response_model=TodoListResponse)
def get_todos(
    is_done: bool | None = None,
    q: str | None = None,
    sort: str | None = None,
    limit: int = 10,
    offset: int = 0
):
    result = todos

    # FILTER theo is_done
    if is_done is not None:
        filtered = []
        for todo in result:
            if todo.is_done == is_done:
                filtered.append(todo)
        result = filtered

    # SEARCH theo title
    if q is not None:
        searched = []
        for todo in result:
            if q.lower() in todo.title.lower():
                searched.append(todo)
        result = searched
    
        # SORT
    if sort is not None:
        reverse = False

        if sort.startswith("-"):
            reverse = True
            sort_field = sort[1:]
        else:
            sort_field = sort

        if sort_field == "created_at":
            result = sorted(result, key=lambda x: x.created_at, reverse=reverse)
    total = len(result)
    result = result[offset: offset + limit]
    return TodoListResponse(
        items=result,
        total=total,
        limit=limit,
        offset=offset
    )

# READ DETAIL (GET /todos/{id})
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# UPDATE (PUT /todos/{id})
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: TodoCreate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            new_todo = Todo(
            id=todo_id, 
            created_at = todo.created_at,
            **updated.dict()
        )
            todos[index] = new_todo
            return new_todo
    raise HTTPException(status_code=404, detail="Todo not found")

# DELETE (DELETE /todos/{id})
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello To-Do API"}
