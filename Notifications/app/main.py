import asyncio
import json
import logging

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from retrying_async import retry

from config import config
from send_email import send_email
from send_notification import send_notification


async def on_email_message(message: AbstractIncomingMessage) -> None:
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


async def on_notification(message: AbstractIncomingMessage) -> None:
    async with message.process():
        body = json.loads(message.body)
        try:
            subject = body.pop("user_id")
            send_notification(
                subject=subject,
                data=body,
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
        await queue.consume(on_email_message)

        queue = await channel.declare_queue("notifications")
        await queue.consume(on_notification)

        await asyncio.Future()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    asyncio.run(main())
