from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


# ===== CREATE SCHEMA =====
class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = None
    is_done: bool = False
    due_date: datetime | None = None


# ===== RESPONSE SCHEMA =====
class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime


# ===== LIST RESPONSE =====
class TodoListResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    limit: int
    offset: int