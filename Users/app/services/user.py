from typing import Union, Dict, Any, List

from app import crud
from app.core import exceptions
from app.models import User
from app.schemas import UserUpdate, UserCreate


class UserService:
    @staticmethod
    def authenticate(db, *, username: str, password: str) -> User:
        user = crud.user.authenticate(
            db, email=username, password=password
        )

        if not user:
            raise exceptions.BadRequestException(message="Incorrect email or password")
        elif not user.is_active:
            raise exceptions.BadRequestException(message="Inactive user")

        return user

    @staticmethod
    def get_user_list(db, *, skip: int, limit: int) -> List[User]:
        return crud.user.get_multi(db, skip=skip, limit=limit)

    @staticmethod
    async def create_user(db, *, obj_in: Union[UserCreate, Dict[str, Any]]) -> User:
        user = crud.user.get_by_email(db, email=obj_in.email)
        if user:
            raise exceptions.BadRequestException(message="The user with this username already exists in the system")

        user = crud.user.create(db, obj_in=obj_in)

        return user

    @staticmethod
    def get_user(db, *, id) -> User:
        user = crud.user.get(db, id=id)

        if not user:
            raise exceptions.NotFoundException(
                message="The user with this username does not exist in the system",
            )

        return user

    @staticmethod
    def get_user_by_email(db, *, email) -> User:
        user = crud.user.get_by_email(db, email=email)

        if not user:
            raise exceptions.NotFoundException(
                message="The user with this username does not exist in the system",
            )

        return user

    @staticmethod
    def update_user(db, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        return crud.user.update(db, db_obj=db_obj, obj_in=obj_in)
