from sqlmodel import Session
from app.module.task_worker.models import TaskWorker, TaskWorkerCreate


def create_task_worker(db: Session, task_worker: TaskWorkerCreate):
    db_task_worker = TaskWorker(
        task_id=task_worker.task_id,
        worker_id=task_worker.worker_id,
    )
    db.add(db_task_worker)
    db.commit()
    db.refresh(db_task_worker)
    return db_task_worker


def get_task_worker(db: Session, task_id: int, worker_id: int):
    return (
        db.query(TaskWorker)
        .filter(TaskWorker.task_id == task_id, TaskWorker.worker_id == worker_id)
        .first()
    )
