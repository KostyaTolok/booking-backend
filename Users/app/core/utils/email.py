import json
from aio_pika import Message, connect
from jinja2 import Environment, FileSystemLoader

from app.core.config import config


async def send_email(*, email: str, subject: str, html: str = None, text: str = None):
    connection = await connect(config.RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("email")

        message = {
            "email": email,
            "subject": subject,
        }

        if html is not None:
            message["html"] = html
        if text is not None:
            message["text"] = text

        # TODO add exchanger && create amqp abstraction ?
        await channel.default_exchange.publish(
            Message(json.dumps(message).encode("utf-8")),
            routing_key=queue.name,
        )


def render_template(template_name, **kwargs):
    environment = Environment(loader=FileSystemLoader(config.TEMPLATES_PATH))
    return environment.get_template(template_name).render(**kwargs)
