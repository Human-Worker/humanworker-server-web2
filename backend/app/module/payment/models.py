from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class PaymentBase(SQLModel):
    amount: float
    currency: str = Field(default="USD")
    timestamp: datetime = Field(default=datetime.utcnow())
    payment_status: str = Field(default="pending")


class Payment(PaymentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(default=None, foreign_key="task.id")
    client_id: int = Field(default=None, foreign_key="client.id")
    worker_id: int = Field(default=None, foreign_key="worker.id")
    stripe_payment_id: Optional[str] = Field(default=None, index=True)
    stripe_card_id: Optional[str] = Field(default=None, index=True)


class PaymentCreate(PaymentBase):
    task_id: int
    client_id: int
    worker_id: int


class PaymentRead(PaymentBase):
    id: int
