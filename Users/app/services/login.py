from datetime import timedelta

from pydantic.error_wrappers import ValidationError
import jwt

from app.core.config import config
from app.core.redis import redis
from app.core.utils import security
from app.core import exceptions


class AuthService:
    @staticmethod
    def decode_token(token: str, refresh: bool = False):
        try:
            payload = security.decode_token(token, refresh)
        except jwt.ExpiredSignatureError:
            raise exceptions.ForbiddenException(message="Token expired")
        except (jwt.DecodeError, ValidationError):
            raise exceptions.ForbiddenException(message="Could not validate credentials")
        return payload

    @staticmethod
    async def get_access_refresh_tokens(user_id: int) -> dict:
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access = security.create_access_token(
            user_id, expires_delta=access_token_expires
        )
        refresh_token_expires = timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh = security.create_refresh_token(
            user_id, expires_delta=refresh_token_expires
        )
        await redis.set(user_id, refresh)

        return {"access_token": access, "refresh_token":  refresh}

    @staticmethod
    async def refresh_tokens(refresh_token: str) -> dict:
        payload = AuthService.decode_token(refresh_token, refresh=True)
        if not await redis.get(payload["sub"]) == refresh_token:
            raise exceptions.ForbiddenException(message="Invalid token")
        return await AuthService.get_access_refresh_tokens(payload["sub"])

