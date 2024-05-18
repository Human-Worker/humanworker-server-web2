from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class TaskBase(SQLModel):
    title: str
    description: str
    deadline: datetime
    status: str = Field(default="open")
    client_escrow: float = Field(default=0.0)
    worker_payout: float = Field(default=0.0)
    stripe_price_id: Optional[str] = Field(default=None, index=True)


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(default=None, foreign_key="client.id")
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())


class TaskCreate(TaskBase):
    client_id: int


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    client_id: int
