from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.payment.models import PaymentCreate, PaymentRead
from app.module.payment.crud import create_payment, get_payment
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.get("/{payment_id}", response_model=PaymentRead)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_payment = get_payment(db, payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment
