from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.task_rating.models import TaskRatingCreate, TaskRatingRead
from app.module.task_rating.crud import create_task_rating, get_task_rating
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=TaskRatingRead)
def create_task_rating_endpoint(
    task_rating: TaskRatingCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return create_task_rating(db, task_rating)


@router.get("/{task_rating_id}", response_model=TaskRatingRead)
def read_task_rating(
    task_rating_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_task_rating = get_task_rating(db, task_rating_id)
    if db_task_rating is None:
        raise HTTPException(status_code=404, detail="TaskRating not found")
    return db_task_rating
