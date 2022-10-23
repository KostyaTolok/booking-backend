import os
from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator
from pydantic.networks import PostgresDsn, AmqpDsn


class Config(BaseSettings):
    ENV: str
    DEBUG: bool
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api"
    API_CURRENT_VERSION: str = "v1"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    SEARCH_SERVICE_API_URL: str

    SECRET_KEY: str

    PAYMENT_INTENT_EXPIRE_MINUTES: int = 15
    REMOVE_EXPIRED_PAYMENT_INTENTS_SECONDS = 60

    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DB_URL: PostgresDsn = None

    @validator("DB_URL")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB', '')}",
        )

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_URL: Optional[AmqpDsn] = None

    RABBITMQ_PAYMENT_EVENTS_EXCHANGE_NAME: str

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

    class Config:
        env_file = ".env"


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