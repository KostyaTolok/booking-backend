from typing import Generator

import aiohttp
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from pydantic.error_wrappers import ValidationError

from app.core.db import SessionLocal
from app.core.http_session import SingletonAiohttp
from app.core.utils.jwt import decode_token
from app.schemas import Token

reusable_oauth2 = OAuth2()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_http_client() -> aiohttp.ClientSession:
    return SingletonAiohttp.get_aiohttp_client()


def get_token_payload(token: str = Depends(reusable_oauth2)) -> Token:
    payload = decode_token(token)
    try:
        token = Token(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
    return token


def get_active_token_payload(
    token_payload: Token = Depends(get_token_payload),
) -> Token:
    if not token_payload.active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return token_payload


def get_active_superuser_token_payload(
    token_payload: Token = Depends(get_active_token_payload),
) -> Token:
    if token_payload.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return token_payload
