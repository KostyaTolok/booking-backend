import json
import logging
import threading

import pika
from django.db import connection as db_connection


class Consumer(threading.Thread):
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        super().__init__()

    def run(self):
        parameters = pika.URLParameters(self.settings.BOOKING_BROKER_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(
            self.settings.BOOKING_QUEUE_NAME,
            durable=True,
        )
        channel.queue_bind(
            exchange=self.settings.BOOKING_EXCHANGE_NAME,
            queue=self.settings.BOOKING_QUEUE_NAME,
        )
        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(
            on_message_callback=self.process_message,
            queue=self.settings.BOOKING_QUEUE_NAME,
            auto_ack=True,
        )
        channel.start_consuming()

    def process_message(self, channel, method, properties, body):
        from booking.models import Booking
        from rooms.models import Room

        try:
            message = json.loads(body.decode())
            self.logger.info(f"Booking received: {message}")
            room_id = message.pop("apartment_id", None)
            rooms = Room.objects.raw(
                """
                SELECT
                    id
                FROM
                    rooms_room
                WHERE
                    id = %s
                """,
                [room_id],
            )
            room_id = rooms[0].id if rooms else None

            with db_connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO booking_booking (user, start_date, end_date, succeeded_at, room_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    [
                        message.get("user_id"),
                        message.get("start_date"),
                        message.get("end_date"),
                        message.get("succeeded_at"),
                        room_id,
                    ],
                )
        except Exception as e:
            self.logger.error(e)
