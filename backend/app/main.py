from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, VARCHAR, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
import os

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

# MySQL connection details
DATABASE_URL = os.getenv("DATABASE_URL","mysql+pymysql://myuser:mypassword@mysql:3306/tododb")


# Database connection and ORM setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# To-Do Model
class TodoItem(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(VARCHAR(length=150), index=True)
    completed = Column(Boolean, default=False)

# Create the tables if they don't exist
Base.metadata.create_all(bind=engine)

# Pydantic model for To-Do items
class TodoItemBase(BaseModel):
    task: str
    completed: bool = False

class TodoItemDB(TodoItemBase):
    id: int

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the To-Do API with MySQL"}

@app.get("/todos", response_model=List[TodoItemDB])
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(TodoItem).all()
    return [{"id": todo.id, "task": todo.task, "completed": todo.completed} for todo in todos]

@app.post("/todos", response_model=TodoItemDB)
async def create_todo(todo: TodoItemBase, db: Session = Depends(get_db)):
    new_todo = TodoItem(task=todo.task, completed=todo.completed)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {"id": new_todo.id, "task": new_todo.task, "completed": new_todo.completed}

@app.put("/todos/{todo_id}", response_model=TodoItemDB)
async def update_todo(todo_id: int, updated_todo: TodoItemBase, db: Session = Depends(get_db)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.task = updated_todo.task
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)
    return {"id": todo.id, "task": todo.task, "completed": todo.completed}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}