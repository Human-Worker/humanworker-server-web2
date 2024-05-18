import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.task.models import Task, TaskCreate
from app.module.task.crud import create_task, get_task, update_task, delete_task


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_task(setup_db):
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        deadline="2024-05-17T00:00:00",
        client_id=1,
    )
    created_task = create_task(setup_db, task_data)
    assert created_task.id is not None
    assert created_task.title == "Test Task"


def test_get_task(setup_db):
    task_data = TaskCreate(
        title="Test Task 2",
        description="Test Description 2",
        deadline="2024-05-17T00:00:00",
        client_id=1,
    )
    created_task = create_task(setup_db, task_data)
    fetched_task = get_task(setup_db, task_id=created_task.id)
    assert fetched_task.title == "Test Task 2"


def test_update_task(setup_db):
    task_data = TaskCreate(
        title="Test Task 3",
        description="Test Description 3",
        deadline="2024-05-17T00:00:00",
        client_id=1,
    )
    created_task = create_task(setup_db, task_data)
    update_data = TaskCreate(
        title="Updated Task 3",
        description="Updated Description 3",
        deadline="2024-06-17T00:00:00",
        client_id=1,
    )
    updated_task = update_task(setup_db, task_id=created_task.id, task=update_data)
    assert updated_task.title == "Updated Task 3"


def test_delete_task(setup_db):
    task_data = TaskCreate(
        title="Test Task 4",
        description="Test Description 4",
        deadline="2024-05-17T00:00:00",
        client_id=1,
    )
    created_task = create_task(setup_db, task_data)
    delete_task(setup_db, task_id=created_task.id)
    deleted_task = get_task(setup_db, task_id=created_task.id)
    assert deleted_task is None
