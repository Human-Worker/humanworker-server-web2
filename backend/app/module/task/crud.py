from sqlmodel import Session
from app.module.task.models import Task, TaskCreate


def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        client_id=task.client_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.deadline = task.deadline
        db_task.client_id = task.client_id
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
