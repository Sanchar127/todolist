# app/repositories/todo_repository.py

from sqlalchemy.orm import Session
from models import TodoItem  # Ensure this import is correct
from schemas import TodoItemBase  # Ensure this import is correct

class TodoRepository:
    @staticmethod
    def get_all_todos(db: Session):
        return db.query(TodoItem).all()

    @staticmethod
    def create_todo(db: Session, todo: TodoItemBase):
        new_todo = TodoItem(task=todo.task, completed=todo.completed)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo

    @staticmethod
    def update_todo(db: Session, todo_id: int, updated_todo: TodoItemBase):
        todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
        if not todo:
            return None
        todo.task = updated_todo.task
        todo.completed = updated_todo.completed
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(db: Session, todo_id: int):
        todo = db.query(TodoItem).filter(TodoItem.id == todo_id).first()
        if not todo:
            return None
        db.delete(todo)
        db.commit()
        return todo
