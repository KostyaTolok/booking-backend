from datetime import datetime, timedelta
from typing import Any, Union

import jwt
from passlib.context import CryptContext

from app.core.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_token(
        subject: Union[str, Any], expires_delta: timedelta = None, refresh: bool = False
):
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        minutes = config.ACCESS_TOKEN_EXPIRE_MINUTES if refresh \
            else config.ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=minutes)

    token_type = "refresh" if refresh else "access"
    to_encode = {"exp": expire, "sub": str(subject), "type": token_type}

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    return create_token(subject, expires_delta, refresh=False)


def create_refresh_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    return create_token(subject, expires_delta, refresh=True)


def decode_token(token: str, refresh: bool = False) -> dict:
    payload = jwt.decode(
        token, config.SECRET_KEY, algorithms=[ALGORITHM]
    )

    token_type = "refresh" if refresh else "access"
    if not payload.get("type") == token_type:
        raise jwt.InvalidTokenError

    return payload


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
