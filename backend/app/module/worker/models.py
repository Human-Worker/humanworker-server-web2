from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.module.user.models import UserBase


class WorkerBase(SQLModel):
    skills: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume: Optional[str] = None
    hourly_rate: Optional[float] = None
    availability: Optional[str] = None
    average_rating: float = Field(default=0.0)


class Worker(WorkerBase, UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class WorkerCreate(WorkerBase, UserBase):
    password: str


class WorkerRead(WorkerBase, UserBase):
    id: int
