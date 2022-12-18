import json

from aio_pika import Message, ExchangeType, DeliveryMode

from app.core.amqp_connection import SingletonAmqp
from app.core.config import config


async def send_payment_event(message: dict):
    connection = await SingletonAmqp.get_amqp_connection()
    channel = await connection.channel()

    exchange = await channel.get_exchange(
        config.RABBITMQ_PAYMENT_EVENTS_EXCHANGE_NAME, ensure=True
    )

    notifications_queue = await channel.declare_queue(
        config.RABBITMQ_NOTIFICATIONS_QUEUE_NAME
    )
    await notifications_queue.bind(exchange)

    message = Message(
        json.dumps(message, default=str).encode("utf-8"),
        delivery_mode=DeliveryMode.PERSISTENT,
    )

    await exchange.publish(message, routing_key="payment")


async def create_payments_exchange():
    connection = await SingletonAmqp.get_amqp_connection()
    channel = await connection.channel()
    await channel.declare_exchange(
        config.RABBITMQ_PAYMENT_EVENTS_EXCHANGE_NAME,
        ExchangeType.FANOUT,
    )
