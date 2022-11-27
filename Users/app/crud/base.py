from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        tablename = self.model.__tablename__
        cols = [f'"{tablename}".{c} AS {self.model.__tablename__}_{c}'
                for c in self.model.__table__.columns.keys()]
        sql = f"""SELECT {", ".join(cols)}
                  FROM "{tablename}"  WHERE "{tablename}".id = {id} LIMIT 1"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)

        return result.scalars().one_or_none()

    def get_or_create(self, db: Session, *, obj_in: CreateSchemaType):
        obj_in_data = jsonable_encoder(obj_in)

        instance = db.query(self.model).filter_by(**obj_in_data).one_or_none()
        if instance:
            return instance

        instance = self.model(**obj_in_data)
        db.add(instance)
        db.commit()

        return instance

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        tablename = self.model.__tablename__
        cols = [f'"{tablename}".{c} AS {self.model.__tablename__}_{c}'
                for c in self.model.__table__.columns.keys()]
        sql = f"""SELECT {", ".join(cols)}
                  FROM "{tablename}" 
                  LIMIT {limit} OFFSET {skip}"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)

        return result.scalars().all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in, exclude_unset=True)
        tablename = self.model.__tablename__
        cols = [f'"{tablename}".{c} AS {self.model.__tablename__}_{c}'
                for c in self.model.__table__.columns.keys()]
        default_cols = {c.name: c.default.arg({}) if callable(c.default.arg) else c.default.arg for c in self.model.__table__.columns if c.default}
        sql = f"""INSERT INTO "{tablename}" ({", ".join(list(obj_in_data.keys()) + list(default_cols.keys()))}) 
                  VALUES ({", ".join(f"'{v}'" for v in list(obj_in_data.values()) + list(default_cols.values()))})
                  RETURNING {", ".join(cols)}"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one()

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        tablename = self.model.__tablename__
        cols = [f'"{tablename}".{c} AS {self.model.__tablename__}_{c}'
                for c in self.model.__table__.columns.keys()]
        sql = f"""UPDATE "{tablename}" 
                  SET {", ".join(f"{k}='{v}'" for k, v in update_data.items())}
                  WHERE "{tablename}".id = {db_obj.id}
                  RETURNING {", ".join(cols)}"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one()

    def remove(self, db: Session, id: int) -> ModelType:
        tablename = self.model.__tablename__
        cols = [f'"{tablename}".{c} AS {self.model.__tablename__}_{c}'
                for c in self.model.__table__.columns.keys()]
        sql = f"""DELETE FROM "{tablename}" 
                   WHERE "{tablename}".id = {id}
                   RETURNING {", ".join(cols)}"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one_or_none()
