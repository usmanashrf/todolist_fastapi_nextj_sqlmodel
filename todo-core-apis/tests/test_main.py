from fastapi.testclient import TestClient
from sqlmodel import Field, Session, SQLModel, create_engine, select

# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency
from todo_core_apis.main import app, get_session, Todo

from todo_core_apis import settings

# https://fastapi.tiangolo.com/tutorial/testing/
# https://realpython.com/python-assert-statement/
# https://understandingdata.com/posts/list-of-python-assert-statements-for-unit-tests/

# postgresql://ziaukhan:oSUqbdELz91i@ep-polished-waterfall-a50jz332.us-east-2.aws.neon.tech/neondb?sslmode=require

def test_read_main():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_write_main():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 

        client = TestClient(app=app)

        todo_content = "buy bread"

        response = client.post("/todos/",
            json={"task": todo_content,"is_done": False}
        )

        data = response.json()

        assert response.status_code == 200
        assert data["task"] == todo_content

def test_read_list_main():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 
        client = TestClient(app=app)

        response = client.get("/todos/")
        assert response.status_code == 200

def test_complete_todo():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app=app)

        # Create a new todo
        todo_content = "complete this task"
        create_response = client.post("/todos/", json={"task": todo_content, "is_done": False})
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Mark the todo as completed
        complete_response = client.put(f"/todos/{todo_id}/complete")
        assert complete_response.status_code == 200
        completed_data = complete_response.json()
        assert completed_data["is_done"] == True

def test_delete_todo():
    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app=app)

        # Create a new todo
        todo_content = "delete this task"
        create_response = client.post("/todos/", json={"task": todo_content, "is_done": False})
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Delete the todo
        delete_response = client.delete(f"/todos/{todo_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() == {"message": "Todo deleted successfully"}

        # Verify that the todo is deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404

def test_database_connection():
    # Create an engine for the test database
    connection_string = str(settings.TEST_DATABASE_URL).replace(
        "postgresql", "postgresql+psycopg"
    )
    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}
    )

    # Create the tables in the test database
    SQLModel.metadata.create_all(engine)

    # Create a new session and add a test Todo item
    with Session(engine) as session:
        test_todo = Todo(task="Test DB Connection", is_done=False)
        session.add(test_todo)
        session.commit()

        # Query the test Todo item from the database
        result = session.exec(select(Todo).where(Todo.task == "Test DB Connection")).first()

        # Assert that the queried Todo item matches the inserted Todo item
        assert result.task == test_todo.task
        assert result.is_done == test_todo.is_done

    # Drop the tables after the test
    SQLModel.metadata.drop_all(engine)