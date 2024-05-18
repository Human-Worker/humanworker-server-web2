from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.task_worker.models import TaskWorkerCreate, TaskWorkerRead
from app.module.task_worker.crud import create_task_worker, get_task_worker
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=TaskWorkerRead)
def create_task_worker_endpoint(
    task_worker: TaskWorkerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return create_task_worker(db, task_worker)


@router.get("/{task_id}/{worker_id}", response_model=TaskWorkerRead)
def read_task_worker(
    task_id: int,
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_task_worker = get_task_worker(db, task_id, worker_id)
    if db_task_worker is None:
        raise HTTPException(status_code=404, detail="TaskWorker not found")
    return db_task_worker
