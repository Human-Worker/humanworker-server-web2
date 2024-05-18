from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    stripe_customer_id: Optional[str] = Field(default=None, index=True)
    address: Optional[str] = None
    phone_number: Optional[str] = None
    date_joined: datetime = Field(default=datetime.utcnow())
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
