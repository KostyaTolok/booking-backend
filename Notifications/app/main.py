import asyncio
import json
import logging

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from retrying_async import retry

from config import config
from send_email import send_email


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        body = json.loads(message.body)
        try:
            send_email(
                sender=config.EMAILS_FROM_EMAIL,
                recipients=(body["email"],),
                subject=body["subject"],
                html=body.get("html", ""),
                text=body.get("text", ""),
            )
        except Exception as e:
            logging.error(e)


@retry(attempts=5, delay=3)
async def get_rabbitmq_connection():
    return await connect(config.RABBITMQ_URL)


async def main() -> None:
    connection = await get_rabbitmq_connection()

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("email")
        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    asyncio.run(main())
