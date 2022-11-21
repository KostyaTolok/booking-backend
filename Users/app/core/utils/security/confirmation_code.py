import string
import secrets

import aioredis

from app.core.config import config


ALGORITHM = "HS256"

redis = aioredis.from_url(config.REDIS_URL, decode_responses=True)


async def get_code(subject: str, interval: int = 2*60) -> str:
    code = (str(secrets.choice(string.digits)) for _ in range(4))
    code = "".join(code)
    await redis.set(subject, code)
    await redis.expire(subject, interval)
    return code


async def verify_code(subject: str, code: str) -> bool:
    value = await redis.get(subject)
    return value == code
