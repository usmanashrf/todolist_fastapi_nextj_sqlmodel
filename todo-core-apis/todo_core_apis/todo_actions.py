from sqlmodel import select
from .models import Todo
from fastapi import HTTPException

def create_todo(session, todo: Todo):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

def get_task(session, todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
def read_todos(session):
    todos = session.exec(select(Todo)).all()
    return todos

def delete_todo(session, todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

def complete_todo(session, todo_id: int)-> Todo:
    todo = session.get(Todo, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.is_done = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
