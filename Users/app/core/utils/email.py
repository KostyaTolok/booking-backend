import json
from aio_pika import Message, connect

from app.core.config import config


async def send_email(*, email_to: str, subject_template: str, html_template: str, environment: str):
    connection = await connect(config.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("email")

        message = {
            "email_to": email_to,
            "subject_template": subject_template,
            "html_template": html_template,
            "environment": environment,
        }

        # TODO add exchanger && create amqp abstraction ?
        await channel.default_exchange.publish(
            Message(json.dumps(message).encode('utf-8')),
            routing_key=queue.name,
        )


async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    message = {
        "email_to": email_to,
        "subject_template": "1",
        "html_template": "1",
        "environment": {
            "username": email,
            "email": email_to,
            "valid_hours": config.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": f"boba/reset-password?token={token}",
        }
    }
    await send_email(**message)


async def send_confirm_email(email_to: str, email: str, code: str) -> None:
    message = {
        "email_to": email_to,
        "subject_template": "1",
        "html_template": "1",
        "environment": {
            "username": email,
            "email": email_to,
            "valid_seconds": config.EMAIL_CONFIRMATION_CODE_EXPIRE_SECONDS,
            "code": code,
        }
    }
    await send_email(**message)
