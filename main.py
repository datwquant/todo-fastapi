from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI()

# Model dùng để CREATE / UPDATE
class TodoCreate(BaseModel):
    title: str
    is_done: bool = False

# Model dùng để RESPONSE
class Todo(TodoCreate):
    id: int

# data trong ram
todos: List[Todo] = []
current_id = 1

# CREATE (POST /todos)
@app.post("/todos", response_model = Todo)
def create_todo(todo: TodoCreate):
    global current_id
    new_todo = Todo(id=current_id, **todo.dict())
    todos.append(new_todo)
    current_id += 1
    return new_todo

# READ LIST (GET /todos)
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

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
            new_todo = Todo(id=todo_id, **updated.dict())
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
