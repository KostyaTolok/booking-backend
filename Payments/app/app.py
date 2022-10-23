import logging

from fastapi import FastAPI
from alembic.config import Config
from alembic import command
from retry import retry
from kafka_logger.handlers import KafkaLoggingHandler

from app.core.config import config
from app.routers import router
from app.tasks import remove_expired_payment_intents
from app.core.http_session import SingletonAiohttp
from app.core.amqp_connection import SingletonAmqp

app = FastAPI()


@app.on_event("startup")
async def startup():
    SingletonAiohttp.get_aiohttp_client()
    await SingletonAmqp.get_amqp_connection()
    await remove_expired_payment_intents()


@app.on_event("shutdown")
async def shutdown():
    await SingletonAiohttp.close_aiohttp_client()
    await SingletonAmqp.close_amqp_connection()


@retry(Exception, tries=5, delay=3)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.DB_URL)
    command.upgrade(alembic_cfg, "head")


# TODO run_migrations() broke logs
run_migrations()

app.include_router(router, prefix=config.API_PREFIX)

KAFKA_BOOTSTRAP_SERVER = "kafka:9092"
TOPIC = "payment"

kafka_handler_obj = KafkaLoggingHandler(
    KAFKA_BOOTSTRAP_SERVER,
    TOPIC,
    security_protocol="PLAINTEXT",
)
logger = logging.getLogger()
logger.addHandler(kafka_handler_obj)
logger.setLevel(logging.INFO)
