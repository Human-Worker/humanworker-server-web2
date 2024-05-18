from sqlmodel import Session
from app.module.client.models import Client, ClientCreate
from app.common.security import hash_password


def create_client(db: Session, client: ClientCreate):
    hashed_password = hash_password(client.password)
    db_client = Client(
        username=client.username,
        email=client.email,
        hashed_password=hashed_password,
        first_name=client.first_name,
        last_name=client.last_name,
        address=client.address,
        phone_number=client.phone_number,
        profile_picture=client.profile_picture,
        bio=client.bio,
        company_name=client.company_name,
        company_website=client.company_website,
        company_address=client.company_address,
        company_phone=client.company_phone,
        average_rating=client.average_rating,
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def get_client_by_email(db: Session, email: str):
    return db.query(Client).filter(Client.email == email).first()
