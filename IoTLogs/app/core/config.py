from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 9000

    LOGGING_LEVEL: str = "INFO"

    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION_NAME: str = ""
    LOGS_TABLE_NAME: str = ""

    class Config:
        env_file = ".env"


@lru_cache
def get_config() -> Config:
    return Config()


config: Config = get_config()
