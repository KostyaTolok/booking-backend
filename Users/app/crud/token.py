from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate


class CRUDToken(CRUDBase[Token, TokenCreate, TokenCreate]):
    def get_by_jti(self, db: Session, *, jti: str) -> Optional[Token]:
        return db.query(Token).filter(Token.jti == jti).first()

    def get_last_by_user_id(self, db: Session, *, user_id: int) -> Optional[Token]:
        return (db.query(Token)
                .filter(Token.user_id == user_id)
                .order_by(desc(Token.id))
                .first())


token = CRUDToken(Token)
