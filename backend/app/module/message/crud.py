from sqlmodel import Session
from app.module.message.models import Message, MessageCreate


def create_message(db: Session, message: MessageCreate):
    db_message = Message(
        content=message.content,
        task_id=message.task_id,
        user_id=message.user_id,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()
