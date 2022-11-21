import json

from aio_pika import Message, ExchangeType, DeliveryMode

from app.core.amqp_connection import SingletonAmqp


async def send_payment_event(message: dict):
    exchange = await SingletonAmqp.get_payments_exchange()

    message = Message(
        json.dumps(message, default=str).encode("utf-8"),
        delivery_mode=DeliveryMode.PERSISTENT,
    )

    await exchange.publish(message, routing_key="payment")
