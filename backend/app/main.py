# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import SessionLocal  # Import the database session from models
from schemas import TodoItemBase, TodoItemDB
from repositories.todo_repository import TodoRepository


# Create FastAPI app instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the To-Do API with MySQL...."}

@app.get("/todos", response_model=List[TodoItemDB])
async def get_todos(db: Session = Depends(get_db)):
    todos = TodoRepository.get_all_todos(db)
    return [{"id": todo.id, "task": todo.task, "completed": todo.completed} for todo in todos]

@app.post("/todos", response_model=TodoItemDB)
async def create_todo(todo: TodoItemBase, db: Session = Depends(get_db)):
    new_todo = TodoRepository.create_todo(db, todo)
    return {"id": new_todo.id, "task": new_todo.task, "completed": new_todo.completed}

@app.put("/todos/{todo_id}", response_model=TodoItemDB)
async def update_todo(todo_id: int, updated_todo: TodoItemBase, db: Session = Depends(get_db)):
    todo = TodoRepository.update_todo(db, todo_id, updated_todo)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"id": todo.id, "task": todo.task, "completed": todo.completed}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = TodoRepository.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
