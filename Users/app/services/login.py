from datetime import datetime, timedelta

from pydantic.error_wrappers import ValidationError
import jwt

from app import crud
from app.core.config import config
from app.core.utils.security import web_token
from app.core import exceptions
from app.schemas.token import BlacklistedTokenCreate


class AuthService:
    @staticmethod
    def decode_token(token: str, refresh: bool = False):
        try:
            payload = web_token.decode_token(token, refresh)
        except jwt.ExpiredSignatureError:
            raise exceptions.ForbiddenException(message="Token expired")
        except (jwt.DecodeError, ValidationError):
            raise exceptions.ForbiddenException(message="Could not validate credentials")
        return payload

    @staticmethod
    async def get_access_refresh_tokens(db, *, user_id: int) -> dict:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access = web_token.create_access_token(
            user_id, expires_delta=access_token_expires
        )
        refresh_token_expires = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh = web_token.create_refresh_token(
            user_id, expires_delta=refresh_token_expires
        )

        return {"access_token": access, "refresh_token": refresh}

    @staticmethod
    async def refresh_tokens(db, *, refresh_token: str) -> dict:
        payload = AuthService.decode_token(refresh_token, refresh=True)

        token = crud.blacklisted_token.get_by_jti(db, jti=payload["jti"])
        if token is not None:
            raise exceptions.ForbiddenException(message="Invalid token")

        token = BlacklistedTokenCreate(
            jti=payload["jti"],
            token=refresh_token,
            expires_at=datetime.fromtimestamp(payload["exp"])
        )
        crud.blacklisted_token.create(db, obj_in=token)

        return await AuthService.get_access_refresh_tokens(db, user_id=payload["sub"])
