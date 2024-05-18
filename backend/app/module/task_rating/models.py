from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class TaskRatingBase(SQLModel):
    rating: float
    review: Optional[str] = None
    timestamp: datetime = Field(default=datetime.utcnow())


class TaskRating(TaskRatingBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(default=None, foreign_key="task.id")
    client_id: int = Field(default=None, foreign_key="client.id")
    worker_id: int = Field(default=None, foreign_key="worker.id")


class TaskRatingCreate(TaskRatingBase):
    task_id: int
    client_id: int
    worker_id: int


class TaskRatingRead(TaskRatingBase):
    id: int
