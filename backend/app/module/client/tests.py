import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.client.models import Client, ClientCreate
from app.module.client.crud import create_client, get_client_by_email


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_client(setup_db):
    client_data = ClientCreate(
        username="testclient",
        email="testclient@example.com",
        password="StrongPassword123",
    )
    created_client = create_client(setup_db, client_data)
    assert created_client.id is not None
    assert created_client.username == "testclient"


def test_get_client_by_email(setup_db):
    client_data = ClientCreate(
        username="testclient2",
        email="testclient2@example.com",
        password="StrongPassword123",
    )
    create_client(setup_db, client_data)
    fetched_client = get_client_by_email(setup_db, email="testclient2@example.com")
    assert fetched_client.email == "testclient2@example.com"
