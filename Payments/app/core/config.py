import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from pydantic.networks import AmqpDsn, KafkaDsn, PostgresDsn


class Config(BaseSettings):
    ENV: str
    DEBUG: bool
    ROOT_PATH: str = ""
    API_PREFIX: str = "/api"
    API_CURRENT_VERSION: str = "v1"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

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
    DB_URL: Optional[PostgresDsn]

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
    RABBITMQ_URL: Optional[AmqpDsn]

    RABBITMQ_PAYMENT_EVENTS_EXCHANGE_NAME: str = "payments"
    RABBITMQ_NOTIFICATIONS_QUEUE_NAME: str = "notifications"

    @validator("RABBITMQ_URL")
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

    KAFKA_LOGGING: bool = False

    ALEMBIC_LOGGING: bool = False
    LOGGING_LEVEL: str = "INFO"

    COLLECT_BOOKINGS_LAMBDA_URL: str = (
        "https://tmyjvl0g7l.execute-api.us-west-2.amazonaws.com/default/collectBookings"
    )

    class Config:
        env_file = ".env"


class DevelopmentConfig(Config):
    DEBUG: str = True
    ENV: str = "development"


class ProductionConfig(Config):
    DEBUG: str = False
    ENV: str = "production"

    KAFKA_LOGGING: bool = True

    KAFKA_HOST: str
    KAFKA_PORT: str
    KAFKA_URL: Optional[KafkaDsn]

    KAFKA_LOGGING_TOPIC_NAME: str

    @validator("KAFKA_URL")
    def assemble_kafka_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"{values.get('KAFKA_HOST')}:{values.get('KAFKA_PORT')}"


def get_config() -> Union[DevelopmentConfig, ProductionConfig]:
    env = os.getenv("ENVIRONMENT", "dev")
    config_type = {
        "dev": DevelopmentConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Union[DevelopmentConfig, ProductionConfig] = get_config()
