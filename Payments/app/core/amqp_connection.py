from typing import Optional

from aio_pika import connect, ExchangeType, Exchange
from aio_pika.abc import AbstractConnection

from app.core.config import config


class SingletonAmqp:
    amqp_connection: Optional[AbstractConnection] = None
    exchange: Optional[Exchange] = None

    @classmethod
    async def get_amqp_connection(cls) -> AbstractConnection:
        if cls.amqp_connection is None:
            cls.amqp_connection = await connect(config.RABBITMQ_URL)
        return cls.amqp_connection

    @classmethod
    async def get_payments_exchange(cls):
        if cls.exchange is None:
            connection = await cls.get_amqp_connection()
            channel = await connection.channel()
            cls.exchange = await channel.declare_exchange(
                config.RABBITMQ_PAYMENT_EVENTS_EXCHANGE_NAME,
                ExchangeType.FANOUT,
            )
        return cls.exchange

    @classmethod
    async def close_amqp_connection(cls) -> None:
        if cls.amqp_connection:
            await cls.amqp_connection.close()
            cls.amqp_connection = None
