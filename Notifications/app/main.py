import asyncio
import json

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from config import config
from send_email import send_email


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        body = json.loads(message.body)
        send_email(email_to=body["email_to"],
                   subject_template=body["subject_template"],
                   html_template=body["html_template"],
                   environment=body["environment"],
                   )


async def main() -> None:
    connection = await connect(config.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("email")
        await queue.consume(on_message)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
