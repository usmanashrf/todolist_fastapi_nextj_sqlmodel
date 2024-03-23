from sqlmodel import Field, SQLModel
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str = Field(index=True)
    is_done: bool = Field(default=False)
    userid: Optional[int] = Field(default=None, foreign_key="user.id")
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str