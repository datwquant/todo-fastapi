from typing import List
from schemas.todo import Todo
from datetime import datetime


class TodoRepository:
    def __init__(self):
        self.todos: List[Todo] = []
        self.current_id = 1

    def create(self, todo_data):
        new_todo = Todo(
            id=self.current_id,
            created_at=datetime.utcnow(),
            **todo_data.dict()
        )
        self.todos.append(new_todo)
        self.current_id += 1
        return new_todo

    def get_all(self):
        return self.todos

    def get_by_id(self, todo_id: int):
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None

    def delete(self, todo_id: int):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                return self.todos.pop(i)
        return None

    def update(self, todo_id: int, updated):
        for i, todo in enumerate(self.todos):
            if todo.id == todo_id:
                new_todo = Todo(
                    id=todo_id,
                    created_at=todo.created_at,
                    **updated.dict()
                )
                self.todos[i] = new_todo
                return new_todo
        return None