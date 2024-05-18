import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.worker.models import Worker, WorkerCreate
from app.module.worker.crud import create_worker, get_worker_by_email


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_worker(setup_db):
    worker_data = WorkerCreate(
        username="testworker",
        email="testworker@example.com",
        password="StrongPassword123",
    )
    created_worker = create_worker(setup_db, worker_data)
    assert created_worker.id is not None
    assert created_worker.username == "testworker"


def test_get_worker_by_email(setup_db):
    worker_data = WorkerCreate(
        username="testworker2",
        email="testworker2@example.com",
        password="StrongPassword123",
    )
    create_worker(setup_db, worker_data)
    fetched_worker = get_worker_by_email(setup_db, email="testworker2@example.com")
    assert fetched_worker.email == "testworker2@example.com"
