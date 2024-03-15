from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine,Session
from .database import get_session, engine
from .todo_actions import create_todo, read_todos, delete_todo, complete_todo, get_task
from .models import Todo
from contextlib import asynccontextmanager

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Hello World API with DB", version="0.0.1")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Session = Depends(get_session)):
    return get_task(session, todo_id)
@app.post("/todos/", response_model=Todo)
def create_todo_endpoint(todo: Todo, session: Session = Depends(get_session)):
    return create_todo(session, todo)

@app.get("/todos/", response_model=list[Todo])
def read_todos_endpoint(session: Session = Depends(get_session)):
    return read_todos(session)

@app.delete("/todos/{todo_id}")
def delete_todo_endpoint(todo_id: int, session: Session = Depends(get_session)):
    return delete_todo(session, todo_id)

@app.put("/todos/{todo_id}/complete")
def complete_todo_endpoint(todo_id: int, session: Session = Depends(get_session)):
    return complete_todo(session, todo_id)
