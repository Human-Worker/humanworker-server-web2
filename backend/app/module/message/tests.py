import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.message.models import Message, MessageCreate
from app.module.message.crud import create_message, get_message


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_message(setup_db):
    message_data = MessageCreate(content="Test Message", task_id=1, user_id=1)
    created_message = create_message(setup_db, message_data)
    assert created_message.id is not None
    assert created_message.content == "Test Message"


def test_get_message(setup_db):
    message_data = MessageCreate(content="Test Message 2", task_id=2, user_id=2)
    created_message = create_message(setup_db, message_data)
    fetched_message = get_message(setup_db, message_id=created_message.id)
    assert fetched_message.content == "Test Message 2"
