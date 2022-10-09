import asyncio
import json
import logging

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from config import config
from send_email import send_email


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        body = json.loads(message.body)
        send_email(
            sender=config.EMAILS_FROM_EMAIL,
            recipients=("booking-mails@mail.ru",),
            subject=body["subject"],
            html=body.get("html", ""),
            text=body.get("text", ""),
        )


async def main() -> None:
    # TODO retry connection
    connection = await connect(config.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("email")
        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    asyncio.run(main())
