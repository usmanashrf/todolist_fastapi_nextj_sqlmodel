from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine,Session
from .database import get_session, engine
from .todo_actions import create_todo, read_todos, delete_todo, complete_todo, get_task
from .models import Todo
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan, title="Todo list API with Fastapi Sqlmodel and Neon postgresql DB", 
              version="0.0.1",
              servers=[
                        {
                            "url": "http://0.0.0.0:8000", 
                            "description": "Development Server"
                        },
                        {
                            "url": "https://hardy-flamingo-concrete.ngrok-free.app", # ADD NGROK URL Here Before Creating GPT Action
                            "description": "Production Server"
                        }
        ])
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
