from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class MessageBase(SQLModel):
    content: str
    timestamp: datetime = Field(default=datetime.utcnow())
    final_submission: bool = Field(default=False)
    is_read: bool = Field(default=False)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    task_id: int = Field(default=None, foreign_key="task.id")


class MessageCreate(MessageBase):
    task_id: int
    user_id: int


class MessageRead(MessageBase):
    id: int
