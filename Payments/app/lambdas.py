import logging
from datetime import date

from aiohttp import ClientSession

from app.core.config import config
from app.core.utils.jwt import encode_token


async def invoke_collect_bookings(
    client: ClientSession,
    user_id: int,
    apartment_id: int,
    start_date: date,
    end_date: date,
):
    data = {
        "apartment_id": apartment_id,
        "start_date": str(start_date),
        "end_date": str(end_date),
    }
    headers = {"Authorization": encode_token({"sub": str(user_id)})}
    async with client.post(
        config.COLLECT_BOOKINGS_LAMBDA_URL, json=data, headers=headers
    ) as response:
        logging.info(f"{data} | status code = {response.status}")
        response.raise_for_status()
