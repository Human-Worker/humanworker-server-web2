from sqlmodel import SQLModel, Field
from datetime import datetime


class TaskWorker(SQLModel, table=True):
    task_id: int = Field(default=None, primary_key=True, foreign_key="task.id")
    worker_id: int = Field(default=None, primary_key=True, foreign_key="worker.id")
    assigned_at: datetime = Field(default=datetime.utcnow())
    completed_at: datetime = Field(default=None)
    time_spent: datetime = Field(default=None)


class TaskWorkerCreate(SQLModel):
    task_id: int
    worker_id: int


class TaskWorkerRead(TaskWorkerCreate):
    assigned_at: datetime
    completed_at: Optional[datetime]
    time_spent: Optional[datetime]
