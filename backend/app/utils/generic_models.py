from __future__ import annotations

from abc import ABC
from datetime import datetime
from enum import Enum
from typing import ClassVar, Optional, Self
from typing_extensions import Unpack
from fastapi import APIRouter, Depends
from pydantic import UUID4, BaseModel, PrivateAttr
import pydantic
from pydantic.config import ConfigDict

from sqlmodel import Field, SQLModel, Session, select
import sqlmodel


# NOTE will be required for making queries to the models
class ModelBase(BaseModel):

    ModelCreate: ClassVar[type["ModelCreate"]] = None
    ModelRead: ClassVar[type["ModelRead"]] = None
    ModelUpdate: ClassVar[type["ModelUpdate"]] = None
    ModelInDB: ClassVar[type["ModelInDB"]] = None

    pass


class ModelCreate(BaseModel):
    ModelBase: ClassVar[type[ModelBase]] = None


class ModelRead(BaseModel):

    ModelBase: ClassVar[type[ModelBase]] = None

    id: UUID4

    created_at: datetime
    last_edited: datetime


class ModelUpdate(BaseModel):

    ModelBase: ClassVar[type[ModelBase]] = None


class ModelInDB(SQLModel, BaseModel):

    ModelBase: ClassVar[type[ModelBase]] = None

    id: UUID4 = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    last_edited: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    @classmethod
    def create(cls, create_data: ModelCreate | dict, session: Session) -> Self:
        return cls(**create_data).save(session)

    @classmethod
    def get_by_id(cls, id: UUID4, session: Session) -> ModelRead:
        return session.exec(select(cls).where(cls.id == id)).first()

    @classmethod
    def get_by_ids(cls, ids: list[UUID4], session: Session) -> list[ModelRead]:
        return session.exec(select(cls).where(cls.id.in_(ids))).all()

    @classmethod
    def get_all(cls, session: Session) -> list[ModelRead]:
        return session.exec(select(cls)).all()

    def update(self, update_data: ModelUpdate | dict, session: Session):
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)
        self.sqlmodel_update(update_data)
        self.save(session=session)

    @classmethod
    def update_by_id(cls, id: UUID4, update_data: ModelUpdate | dict, session: Session):
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)
        session.exec(sqlmodel.update(cls).where(cls.id == id).values(update_data))

    @classmethod
    def update_by_ids(
        cls, ids: list[UUID4], update_data: ModelUpdate | dict, session: Session
    ):
        if isinstance(update_data, BaseModel):
            update_data = update_data.model_dump(exclude_unset=True)
        from sqlalchemy import bindparam

        stmt = cls.__table__.update().where(cls.id.in_(ids)).values(update_data)
        session.execute(stmt, [{"id": id} for id in ids])
        session.commit()

    def delete(self, session: Session) -> None:
        session.delete(self)
        session.commit()

    @classmethod
    def delete_by_id(cls, id: UUID4, session: Session) -> None:
        session.delete(cls.get_by_id(id, session))
        session.commit()

    @classmethod
    def delete_by_ids(cls, ids: list[UUID4], session: Session) -> None:
        from sqlalchemy import bindparam

        stmt = cls.__table__.delete().where(cls.id == bindparam("id"))
        session.execute(stmt, [{"id": id} for id in ids])
        session.commit()

    def save(self, session: Session) -> Self:
        session.add(self)
        session.commit()
        session.refresh(self)
        return self


def register_crud_model(
    router: APIRouter,
    /,
    *,
    T_ModelBase: ModelBase,
    T_ModelCreate: ModelCreate,
    T_ModelRead: ModelRead,
    T_ModelUpdate: ModelUpdate,
    T_ModelInDB: ModelInDB,
) -> APIRouter:

    # wire up everything
    T_ModelBase.ModelCreate = T_ModelCreate
    T_ModelBase.ModelRead = T_ModelRead
    T_ModelBase.ModelUpdate = T_ModelUpdate
    T_ModelBase.ModelInDB = T_ModelInDB

    T_ModelCreate.ModelBase = T_ModelBase
    T_ModelRead.ModelBase = T_ModelBase
    T_ModelUpdate.ModelBase = T_ModelBase

    router = (APIRouter(),)
    mount_crud_endpoints(
        router,
        T_ModelCreate=T_ModelCreate,
        T_ModelRead=T_ModelRead,
        T_ModelUpdate=T_ModelUpdate,
        T_ModelInDB=T_ModelInDB,
    )


def mount_crud_endpoints(
    router: APIRouter,
    /,
    *,
    T_ModelCreate: ModelCreate,
    T_ModelRead: ModelRead,
    T_ModelUpdate: ModelUpdate,
    T_ModelInDB: ModelInDB,
) -> APIRouter:

    @router.post(
        f"/",
        responses={
            200: {"model": T_ModelRead},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            409: {"description": "Conflict"},
            500: {"description": "Internal server error"},
        },
    )
    def create(
        create_data: T_ModelCreate, session: Session = Depends(get_session)
    ) -> T_ModelRead:
        db_instance = T_ModelInDB.create(create_data, session=session)
        read_instance = T_ModelRead.from_orm(db_instance)
        return read_instance

    @router.get(
        f"/<id>",
        responses={
            200: {"model": T_ModelRead},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def get_by_id(id: UUID4, session: Session = Depends(get_session)) -> T_ModelRead:
        return T_ModelInDB.get_by_id(id, session=session)

    @router.get(
        f"/multiple/<ids>",
        responses={
            200: {"model": list[T_ModelRead]},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def get_by_ids(
        ids: str, session: Session = Depends(get_session)
    ) -> list[T_ModelRead]:
        ids = [UUID4(id) for id in ids.split(",")]
        return T_ModelInDB.get_by_ids(ids, session=session)

    @router.get(
        f"/",
        responses={
            200: {"model": list[T_ModelRead]},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def get_all(session: Session = Depends(get_session)) -> list[T_ModelRead]:
        return T_ModelInDB.get_all(session=session)

    @router.put(
        f"/<id>",
        responses={
            200: {"description": "No content"},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def update_by_id(
        id: UUID4, update_data: T_ModelUpdate, session: Session = Depends(get_session)
    ) -> None:
        T_ModelInDB.update_by_id(id, update_data, session=session)

    @router.put(
        f"/<ids>",
        responses={
            200: {"description": "No content"},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def update_by_ids(
        ids: str, update_data: T_ModelUpdate, session: Session = Depends(get_session)
    ) -> None:
        ids = [UUID4(id) for id in ids.split(",")]
        T_ModelInDB.update_by_ids(ids, update_data, session=session)

    @router.delete(
        f"/<id>",
        responses={
            200: {"description": "No content"},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def delete(id: UUID4, session: Session = Depends(get_session)) -> None:
        T_ModelInDB.delete(id, session=session)

    @router.delete(
        f"/multiple/<ids>",
        responses={
            200: {"description": "No content"},
            401: {"description": "Unauthorized"},
            403: {"description": "Forbidden"},
            404: {"description": "Not found"},
            500: {"description": "Internal server error"},
        },
    )
    def delete_by_ids(ids: str, session: Session = Depends(get_session)) -> None:
        ids = [UUID4(id) for id in ids.split(",")]
        T_ModelInDB.delete_by_ids(ids, session=session)

    return router
