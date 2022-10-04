from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Tokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class Token(BaseModel):
    jti: str
    exp: int
    sub: str
    type: str
    role: Optional[str]
    active: Optional[bool]
    extra: Optional[dict]


class TokenCreate(BaseModel):
    user_id: int
    jti: str
    token: str
    expires_at: datetime


class BlacklistedTokenCreate(BaseModel):
    token_id: int
