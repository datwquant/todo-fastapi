from sqlalchemy.orm import Session
from models.todo import Todo


class TodoRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data):
        todo = Todo(**data.model_dump())
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def get_all(self, limit=10, offset=0):
        return (
            self.db.query(Todo)
            .offset(offset)
            .limit(limit)
            .all()
        )

    def count(self):
        return self.db.query(Todo).count()

    def get_by_id(self, todo_id: int):
        return (
            self.db.query(Todo)
            .filter(Todo.id == todo_id)
            .first()
        )

    def delete(self, todo_id: int):
        todo = self.get_by_id(todo_id)
        if not todo:
            return None
        self.db.delete(todo)
        self.db.commit()
        return todo

    def patch(self, todo_id: int, data: dict):
        todo = self.get_by_id(todo_id)
        if not todo:
            return None

        for key, value in data.items():
            setattr(todo, key, value)

        self.db.commit()
        self.db.refresh(todo)
        return todo