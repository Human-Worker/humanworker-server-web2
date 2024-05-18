from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.user.models import UserCreate, UserRead
from app.module.user.crud import create_user, get_user_by_email
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


def validate_password_strength(password: str):
    import re

    if (
        len(password) < 8
        or not re.search("[a-z]", password)
        or not re.search("[A-Z]", password)
        or not re.search("[0-9]", password)
    ):
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long and contain an uppercase letter, a lowercase letter, and a digit.",
        )


@router.post("/", response_model=UserRead)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    validate_password_strength(user.password)
    return create_user(db, user)


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_user = get_user_by_email(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
