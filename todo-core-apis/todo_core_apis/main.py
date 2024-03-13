# fastapi_neon/main.py

from contextlib import asynccontextmanager

from typing import Union, Optional

from todo_core_apis import settings

from sqlmodel import Field, Session, SQLModel, create_engine, select



from fastapi import FastAPI, HTTPException



class Todo(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    task: str = Field(index=True)
    is_done:bool = Field(default=False)



# only needed for psycopg 3 - replace postgresql

# with postgresql+psycopg in settings.DATABASE_URL

connection_string = str(settings.DATABASE_URL).replace(

    "postgresql", "postgresql+psycopg"

)



# recycle connections after 5 minutes

# to correspond with the compute scale down

engine = create_engine(

    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300

)



def create_db_and_tables():

    SQLModel.metadata.create_all(engine)



# The first part of the function, before the yield, will

# be executed before the application starts

@asynccontextmanager

async def lifespan(app: FastAPI):

    print("Creating tables..")

    create_db_and_tables()

    yield



app = FastAPI(lifespan=lifespan)



@app.get("/")

def read_root():

    return {"Hello": "World"}



@app.post("/todos/")

def create_todo(todo: Todo):

    with Session(engine) as session:

        session.add(todo)

        session.commit()

        session.refresh(todo)

        return todo



@app.get("/todos/")

def read_todos():

    with Session(engine) as session:

        todos = session.exec(select(Todo)).all()

        return todos
    

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}

@app.put("/todos/{todo_id}/complete")
def complete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.is_done = True
        session.add(todo)
        session.commit()
        return todo