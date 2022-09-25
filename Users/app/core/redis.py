import aioredis

from app.core.config import config

# TODO create abstraction
redis = aioredis.from_url(config.REDIS_URL, decode_responses=True)
