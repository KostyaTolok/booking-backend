from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.core.config import config
from app.core.db import SessionLocal
from app.core import exceptions
from app.core.utils.security.jwt import tokens
from app.services.user import UserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.API_PREFIX}/{config.API_CURRENT_VERSION}/auth/login/form"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    payload = tokens.AccessToken(token=token)
    user = UserService.get_user(db, id=payload["sub"])
    if not user:
        raise exceptions.NotFoundException(message="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise exceptions.ForbiddenException(message="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise exceptions.ForbiddenException(
            message="The user doesn't have enough privileges"
        )
    return current_user
