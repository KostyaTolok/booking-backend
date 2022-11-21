import logging

from fastapi import FastAPI
from alembic.config import Config
from alembic import command
from retrying_async import retry
from kafka_logger.handlers import KafkaLoggingHandler

from app.core.config import config
from app.routers import router
from app.tasks import remove_expired_payment_intents
from app.core.http_session import SingletonAiohttp
from app.core.amqp_connection import SingletonAmqp


app = FastAPI(root_path=config.ROOT_PATH)


@retry(attempts=5, delay=3)
async def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.DB_URL)
    command.upgrade(alembic_cfg, "head")


@retry(attempts=5, delay=5)
async def logging_setup():
    kafka_handler_obj = KafkaLoggingHandler(
        config.KAFKA_URL,
        config.KAFKA_LOGGING_TOPIC_NAME,
        security_protocol="PLAINTEXT",
    )
    logger = logging.getLogger()
    logger.addHandler(kafka_handler_obj)
    logger.setLevel(logging.INFO)


@retry(attempts=5, delay=3)
async def create_connections():
    SingletonAiohttp.get_aiohttp_client()
    await SingletonAmqp.get_payments_exchange()


async def close_connections():
    await SingletonAiohttp.close_aiohttp_client()
    await SingletonAmqp.close_amqp_connection()


@app.on_event("startup")
async def startup():
    if config.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    await create_connections()

    await remove_expired_payment_intents()

    # TODO run_migrations() broke logs
    await run_migrations()

    if config.KAFKA_LOGGING:
        await logging_setup()


@app.on_event("shutdown")
async def shutdown():
    await close_connections()


app.include_router(router, prefix=config.API_PREFIX)
