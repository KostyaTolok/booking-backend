import os
import secrets
from typing import List, Optional, Dict, Any

from pydantic import BaseSettings, AnyHttpUrl, validator
from dotenv import load_dotenv
from pydantic.networks import EmailStr, AmqpDsn

load_dotenv()


class Config(BaseSettings):
    ENV: str = None
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT")
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_URL: Optional[AmqpDsn] = None

    @validator("RABBITMQ_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            user=values.get("RABBITMQ_USER"),
            password=values.get("RABBITMQ_PASSWORD"),
            host=values.get("RABBITMQ_HOST"),
            port=values.get("RABBITMQ_PORT"),
        )

    SECRET_KEY: str = secrets.token_urlsafe(32)

    EMAILS_FROM_EMAIL: EmailStr = os.getenv("EMAIL")
    EMAILS_FROM_NAME: Optional[str] = None


class DevelopmentConfig(Config):
    ENV: str = "development"
    pass


class ProductionConfig(Config):
    ENV: str = "production"


def get_config():
    env = os.getenv("ENVIRONMENT", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
