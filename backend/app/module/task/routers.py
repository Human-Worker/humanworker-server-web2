from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.task.models import TaskCreate, TaskRead
from app.module.task.crud import create_task, get_task, update_task, delete_task
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task_endpoint(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return create_task(db, task)


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_task = get_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_task = update_task(db, task_id, task)
    return db_task


@router.delete("/{task_id}")
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_task = delete_task(db, task_id)
    return {"detail": "Task deleted successfully"}
