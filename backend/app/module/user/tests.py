import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.user.models import User, UserCreate
from app.module.user.crud import create_user, get_user_by_email


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_user(setup_db):
    user_data = UserCreate(
        username="testuser", email="testuser@example.com", password="StrongPassword123"
    )
    created_user = create_user(setup_db, user_data)
    assert created_user.id is not None
    assert created_user.username == "testuser"


def test_get_user_by_email(setup_db):
    user_data = UserCreate(
        username="testuser2",
        email="testuser2@example.com",
        password="StrongPassword123",
    )
    create_user(setup_db, user_data)
    fetched_user = get_user_by_email(setup_db, email="testuser2@example.com")
    assert fetched_user.email == "testuser2@example.com"
