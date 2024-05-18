from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.message.models import MessageCreate, MessageRead
from app.module.message.crud import create_message, get_message
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=MessageRead)
def create_message_endpoint(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return create_message(db, message)


@router.get("/{message_id}", response_model=MessageRead)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_message = get_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message
