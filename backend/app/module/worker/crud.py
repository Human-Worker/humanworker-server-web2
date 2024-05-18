from sqlmodel import Session
from app.module.worker.models import Worker, WorkerCreate
from app.common.security import hash_password


def create_worker(db: Session, worker: WorkerCreate):
    hashed_password = hash_password(worker.password)
    db_worker = Worker(
        username=worker.username,
        email=worker.email,
        hashed_password=hashed_password,
        first_name=worker.first_name,
        last_name=worker.last_name,
        address=worker.address,
        phone_number=worker.phone_number,
        profile_picture=worker.profile_picture,
        bio=worker.bio,
        skills=worker.skills,
        portfolio_url=worker.portfolio_url,
        resume=worker.resume,
        hourly_rate=worker.hourly_rate,
        availability=worker.availability,
        average_rating=worker.average_rating,
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def get_worker_by_email(db: Session, email: str):
    return db.query(Worker).filter(Worker.email == email).first()
