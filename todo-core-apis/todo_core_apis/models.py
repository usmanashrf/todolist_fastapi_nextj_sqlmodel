from sqlmodel import Field, SQLModel
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task: str = Field(index=True)
    is_done: bool = Field(default=False)
