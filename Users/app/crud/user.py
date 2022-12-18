from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.utils.security.password import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        tablename = self.model.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}" 
                  WHERE "{tablename}".email = '{email}'
                  LIMIT 1"""
        stmt = db.query(self.model).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one_or_none()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        data = {
            "email": obj_in.email,
            "hashed_password": get_password_hash(obj_in.password),
            "full_name": obj_in.full_name,
        }
        return super().create(
            db,
            obj_in=data,
        )

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
