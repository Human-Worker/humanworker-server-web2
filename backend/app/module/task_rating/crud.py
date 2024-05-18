from sqlmodel import Session
from app.module.task_rating.models import TaskRating, TaskRatingCreate


def create_task_rating(db: Session, task_rating: TaskRatingCreate):
    db_task_rating = TaskRating(
        task_id=task_rating.task_id,
        client_id=task_rating.client_id,
        worker_id=task_rating.worker_id,
        rating=task_rating.rating,
        review=task_rating.review,
    )
    db.add(db_task_rating)
    db.commit()
    db.refresh(db_task_rating)
    return db_task_rating


def get_task_rating(db: Session, task_rating_id: int):
    return db.query(TaskRating).filter(TaskRating.id == task_rating_id).first()
