import asyncio
import json
import os
from dotenv import load_dotenv

import aio_pika

load_dotenv()

BOOKING_BROKER_URL = os.getenv("BOOKING_BROKER_URL")
BOOKING_QUEUE_NAME = os.getenv("BOOKING_QUEUE_NAME")


async def consume_message():
    connection = await aio_pika.connect_robust(BOOKING_BROKER_URL, loop=asyncio.get_running_loop())
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(BOOKING_QUEUE_NAME, durable=True)
    await queue.consume(process_message)
    try:
        await asyncio.Future()
    finally:
        await connection.close()


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        try:
            message = json.loads(message.body.decode())
            print(f"Message received: {message}")
        except Exception as e:
            print(e)
