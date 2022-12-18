from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.crud.base import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenCreate]):
    def get_by_jti(self, db: Session, *, jti: str) -> Optional[Token]:
        tablename = self.model.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}"
                  WHERE "{tablename}".jti = '{jti}'
                  LIMIT 1"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one_or_none()

    def get_last_by_user_id(self, db: Session, *, user_id: int) -> Optional[Token]:
        tablename = self.model.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}"
                  WHERE "{tablename}".user_id = '{user_id}'
                  ORDER BY "{tablename}".id desc
                  LIMIT 1"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one_or_none()


token = CRUDToken(Token)
