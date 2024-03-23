from sqlmodel import select
from .models import Todo
from fastapi import HTTPException

def create_todo(session, todo: Todo, userid: int):
    todo.userid = userid
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

def get_task(session, todo_id: int, userid: int):
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.userid == userid)).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
def read_todos(session, userid: int):
    todos = session.exec(select(Todo).where(Todo.userid == userid)).all()
    return todos

def delete_todo(session, todo_id: int, userid: int):
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.userid == userid)).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}

def complete_todo(session, todo_id: int, userid: int)-> Todo:
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.userid == userid)).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.is_done = True
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
