import json

from cent import Client

from config import config


centrifugo_client = Client(
    config.CENTRIFUGO_API_URL,
    api_key=config.CENTRIFUGO_API_KEY,
    timeout=1,
)


def send_notification(
        subject: str,
        data: dict,
):
    channel = f"{config.CENTRIFUGO_CHAT_NAMESPACE_NAME}:user#{subject}"
    data_json = json.dumps(data)
    centrifugo_client.publish(channel, data_json)
