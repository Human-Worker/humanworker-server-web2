from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.worker.models import WorkerCreate, WorkerRead
from app.module.worker.crud import create_worker, get_worker_by_email
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=WorkerRead)
def create_worker_endpoint(
    worker: WorkerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_worker = get_worker_by_email(db, email=worker.email)
    if db_worker:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_worker(db, worker)


@router.get("/{worker_id}", response_model=WorkerRead)
def read_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_worker = get_worker_by_email(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker
