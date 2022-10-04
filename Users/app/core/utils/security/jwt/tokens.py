from datetime import timedelta, datetime
from typing import Union
from uuid import uuid4

import jwt
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.core.config import config
from app.core.utils.security.jwt.exceptions import InvalidToken

ALGORITHM = "HS256"


class Token:
    token_type = None
    lifetime = None
    payload: dict = None
    token_db: models.Token = None
    token_str: str = None

    def __init__(self, token: Union[str, models.Token] = None, verify=True):
        if self.token_type is None or self.lifetime is None:
            raise ValueError("Cannot create token with no type or lifetime")

        if isinstance(token, models.Token):
            self.token_db = token
            self.token_str = token.token
        else:
            self.token_str = token

        self.current_time = datetime.utcnow()

        if token is not None:
            self.payload = self._decode_token(self.token_str)
            if verify:
                self.verify()
        else:
            self.payload = {
                "jti": uuid4().hex,
                "type": self.token_type,
            }
            self.set_exp(timedelta(minutes=self.lifetime))

    @staticmethod
    def _decode_token(token: str):
        try:
            payload = jwt.decode(
                token, config.SECRET_KEY, algorithms=[ALGORITHM]
            )
        except (jwt.exceptions.InvalidTokenError, jwt.exceptions.ExpiredSignatureError):
            raise InvalidToken("Token is invalid or expired")

        return payload

    @staticmethod
    def _encode_token(payload):
        return jwt.encode(payload, config.SECRET_KEY, algorithm=ALGORITHM)

    def verify(self):
        if self.payload.get("type") != self.token_type:
            raise InvalidToken("Token is invalid or expired")

    def for_user(self, subject):
        self.payload["sub"] = subject
        return self

    def set_exp(self, delta: timedelta):
        self.payload["exp"] = self.current_time + delta

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def __str__(self):
        return self._encode_token(self.payload)

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload


class BlacklistToken(Token):
    if config.TOKEN_BLACKLIST:
        def __init__(
                self,
                db: Session,
                token: Union[str, models.Token] = None,
                verify=True
        ):
            self.db = db
            super().__init__(token, verify)

        def verify(self):
            self.check_blacklist()
            super().verify()

        def check_blacklist(self):
            jti = self.payload["jti"]
            if crud.token.get_by_jti(self.db, jti=jti).blacklist:
                raise InvalidToken("Token is blacklisted")

        def _create_token_db(self) -> models.Token:
            token_in = schemas.TokenCreate(
                user_id=self.payload["sub"],
                jti=self.payload["jti"],
                token=str(self),
                expires_at=self.payload["exp"]
            )
            self.token_db = crud.token.create(self.db, obj_in=token_in)
            return self.token_db

        def _get_token_db(self) -> models.Token:
            if self.token_db:
                return self.token_db

            self.token_db = crud.token.get_by_jti(self.db, jti=self.payload["jti"])
            if self.token_db:
                return self.token_db

            return self._create_token_db()

        def blacklist(self):
            token_db = self._get_token_db()
            blacklisted_token_in = schemas.BlacklistedTokenCreate(token_id=token_db.id)
            return crud.blacklisted_token.get_or_create(self.db, obj_in=blacklisted_token_in)

        def for_user(self, subject):
            super().for_user(subject)
            self._create_token_db()
            return self


class AccessToken(Token):
    token_type = "access"
    lifetime = config.ACCESS_TOKEN_EXPIRE_MINUTES


class RefreshToken(BlacklistToken):
    token_type = "refresh"
    lifetime = config.REFRESH_TOKEN_EXPIRE_MINUTES
