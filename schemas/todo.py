from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    is_done: bool = False


class Todo(TodoCreate):
    id: int
    created_at: datetime


class TodoListResponse(BaseModel):
    items: List[Todo]
    total: int
    limit: int
    offset: int