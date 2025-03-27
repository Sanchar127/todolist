# app/schemas.py
from pydantic import BaseModel

class TodoItemBase(BaseModel):
    task: str
    completed: bool = False

class TodoItemDB(TodoItemBase):
    id: int
