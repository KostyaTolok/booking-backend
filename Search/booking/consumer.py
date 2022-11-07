import json
import logging
import threading

import pika


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
        channel.basic_qos(prefetch_count=10)
        channel.basic_consume(
            on_message_callback=self.process_message, queue=self.settings.BOOKING_QUEUE_NAME, auto_ack=True
        )
        channel.start_consuming()

    def process_message(self, channel, method, properties, body):
        from booking.models import Booking
        from rooms.models import Room

        try:
            message = json.loads(body.decode())
            self.logger.info(f"Booking received: {message}")
            room_id = message.pop("apartment_id", None)
            room = Room.objects.get(id=room_id)
            Booking.objects.create(**message, room=room)
        except Exception as e:
            self.logger.error(e)