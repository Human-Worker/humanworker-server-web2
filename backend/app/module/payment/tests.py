import pytest
from sqlmodel import Session
from app.common.database import engine, SQLModel
from app.module.payment.models import Payment, PaymentCreate
from app.module.payment.crud import create_payment, get_payment


@pytest.fixture(scope="module")
def setup_db():
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    SQLModel.metadata.drop_all(engine)


def test_create_payment(setup_db):
    payment_data = PaymentCreate(
        amount=100.0, currency="USD", task_id=1, client_id=1, worker_id=1
    )
    created_payment = create_payment(setup_db, payment_data)
    assert created_payment.id is not None
    assert created_payment.amount == 100.0


def test_get_payment(setup_db):
    payment_data = PaymentCreate(
        amount=200.0, currency="USD", task_id=2, client_id=2, worker_id=2
    )
    created_payment = create_payment(setup_db, payment_data)
    fetched_payment = get_payment(setup_db, payment_id=created_payment.id)
    assert fetched_payment.amount == 200.0
