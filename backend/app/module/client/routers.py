from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.module.client.models import ClientCreate, ClientRead
from app.module.client.crud import create_client, get_client_by_email
from app.common.dependencies.auth import get_current_user
from app.common.dependencies.db import get_db

router = APIRouter()


@router.post("/", response_model=ClientRead)
def create_client_endpoint(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_client = get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_client(db, client)


@router.get("/{client_id}", response_model=ClientRead)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_client = get_client_by_email(db, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client
