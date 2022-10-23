import os
from typing import List, Optional, Dict, Any

from pydantic import BaseSettings, AnyHttpUrl, validator
from dotenv import load_dotenv
from pydantic.networks import PostgresDsn, AmqpDsn

load_dotenv()


class Config(BaseSettings):
    ENV: str = None
    DEBUG: bool = None
    ROOT_PATH: str = os.getenv("ROOT_PATH", "")
    API_PREFIX: str = "/api"
    API_CURRENT_VERSION: str = "v1"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_BLACKLIST: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    USERS_OPEN_REGISTRATION: bool = False

    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASS: str = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DB_HOST: str = os.getenv("POSTGRES_HOST")
    DB_PORT: str = os.getenv("POSTGRES_PORT")
    DB_URL: Optional[PostgresDsn] = None

    @validator("DB_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("DB_USER"),
            password=values.get("DB_PASS"),
            host=values.get("DB_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            path=f"/{values.get('DB_NAME') or ''}",
        )

    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_URL: Optional[AmqpDsn] = None

    @validator("RABBITMQ_URL", pre=True)
    def assemble_rabbit_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            user=values.get("RABBITMQ_USER"),
            password=values.get("RABBITMQ_PASSWORD"),
            host=values.get("RABBITMQ_HOST"),
            port=values.get("RABBITMQ_PORT"),
        )

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 8
    EMAIL_CONFIRMATION_CODE_EXPIRE_SECONDS: int = 120


class DevelopmentConfig(Config):
    DEBUG: str = True
    ENV: str = "development"
    pass


class ProductionConfig(Config):
    DEBUG: str = False
    ENV: str = "production"


def get_config():
    env = os.getenv("ENVIRONMENT", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
