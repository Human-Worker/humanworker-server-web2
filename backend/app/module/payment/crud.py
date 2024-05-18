from sqlmodel import Session
from app.module.payment.models import Payment, PaymentCreate


def create_payment(db: Session, payment: PaymentCreate):
    db_payment = Payment(
        amount=payment.amount,
        currency=payment.currency,
        task_id=payment.task_id,
        client_id=payment.client_id,
        worker_id=payment.worker_id,
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()
