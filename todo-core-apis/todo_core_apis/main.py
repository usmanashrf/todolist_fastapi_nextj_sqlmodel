from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel, create_engine,Session
from typing import Annotated

from todo_core_apis.authorization import get_current_user
from .database import get_session, engine
from .todo_actions import create_todo, read_todos, delete_todo, complete_todo, get_task
from .models import Todo, User
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)],current_user: User = Depends(get_current_user)):
    return get_task(session, todo_id, current_user.id)
@app.post("/todos/", response_model=Todo)
def create_todo_endpoint(todo: Todo, session: Annotated[Session, Depends(get_session)],current_user: User = Depends(get_current_user)):
    return create_todo(session, todo, current_user.id)

@app.get("/todos/", response_model=list[Todo])
def read_todos_endpoint(session: Annotated[Session, Depends(get_session)],current_user: User = Depends(get_current_user)):
    return read_todos(session, current_user.id)

@app.delete("/todos/{todo_id}")
def delete_todo_endpoint(todo_id: int, session: Annotated[Session, Depends(get_session)],current_user: User = Depends(get_current_user)):
    return delete_todo(session, todo_id, current_user.id)

@app.put("/todos/{todo_id}/complete")
def complete_todo_endpoint(todo_id: int, session: Annotated[Session, Depends(get_session)],current_user: User = Depends(get_current_user)):
    return complete_todo(session, todo_id, current_user.id)


app.include_router(auth.router, prefix="/auth")