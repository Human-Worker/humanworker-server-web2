from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.module.user.models import UserBase


class ClientBase(SQLModel):
    company_name: Optional[str] = None
    company_website: Optional[str] = None
    company_address: Optional[str] = None
    company_phone: Optional[str] = None
    average_rating: float = Field(default=0.0)


class Client(ClientBase, UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ClientCreate(ClientBase, UserBase):
    password: str


class ClientRead(ClientBase, UserBase):
    id: int
