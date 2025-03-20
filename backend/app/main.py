from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from different origins (like localhost:5173)
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for to-do items
todo_list = []

class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do APIs"}

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todo_list

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todo_list.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todo_list
    todo_list = [todo for todo in todo_list if todo.id != todo_id]
    return {"message": "Todo deleted successfully"}
