import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.task_rating.models import TaskRating, TaskRatingCreate
from app.module.task_rating.crud import create_task_rating, get_task_rating


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_task_rating(setup_db):
    task_rating_data = TaskRatingCreate(
        task_id=1, client_id=1, worker_id=1, rating=4.5, review="Great work!"
    )
    created_task_rating = create_task_rating(setup_db, task_rating_data)
    assert created_task_rating.id is not None
    assert created_task_rating.rating == 4.5


def test_get_task_rating(setup_db):
    task_rating_data = TaskRatingCreate(
        task_id=2, client_id=2, worker_id=2, rating=5.0, review="Excellent work!"
    )
    created_task_rating = create_task_rating(setup_db, task_rating_data)
    fetched_task_rating = get_task_rating(
        setup_db, task_rating_id=created_task_rating.id
    )
    assert fetched_task_rating.rating == 5.0
