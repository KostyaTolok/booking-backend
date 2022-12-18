import jwt
from fastapi import HTTPException

from app.core.config import config

ALGORITHM = "HS256"


def decode_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
    except (jwt.exceptions.InvalidTokenError, jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(status_code=403, detail="Token is invalid or expired")

    return payload


def encode_token(payload: dict):
    return jwt.encode(payload, config.SECRET_KEY, algorithm=ALGORITHM)
