import base64
import hashlib
import hmac

import pyotp

from app.core.config import config

ALGORITHM = "HS256"


def get_hash_base32(subject: str):
    dig = hmac.new(config.SECRET_KEY.encode("UTF-8"),
                   msg=subject.encode("UTF-8"),
                   digestmod=hashlib.sha256).digest()
    secret = base64.b32encode(dig).decode()
    return secret


def get_totp(subject: str, interval: int = None):
    if interval is None:
        interval = config.EMAIL_CONFIRMATION_CODE_EXPIRE_SECONDS

    secret = get_hash_base32(subject)
    totp = pyotp.TOTP(secret, interval=interval)
    return totp


def get_code(subject: str, interval: int = None) -> str:
    totp = get_totp(subject, interval)
    return totp.now()


def verify_code(subject: str, code: str, interval: int = None) -> bool:
    totp = get_totp(subject, interval)
    return totp.verify(code)
