import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.task_worker.models import TaskWorker, TaskWorkerCreate
from app.module.task_worker.crud import create_task_worker, get_task_worker


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_task_worker(setup_db):
    task_worker_data = TaskWorkerCreate(task_id=1, worker_id=1)
    created_task_worker = create_task_worker(setup_db, task_worker_data)
    assert created_task_worker.task_id == 1
    assert created_task_worker.worker_id == 1


def test_get_task_worker(setup_db):
    task_worker_data = TaskWorkerCreate(task_id=2, worker_id=2)
    created_task_worker = create_task_worker(setup_db, task_worker_data)
    fetched_task_worker = get_task_worker(setup_db, task_id=2, worker_id=2)
    assert fetched_task_worker.task_id == 2
    assert fetched_task_worker.worker_id == 2
