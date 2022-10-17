import aiohttp
from pydantic.error_wrappers import ValidationError
from fastapi import HTTPException
from aiohttp import ClientSession

from app import schemas


class ApartmentServices:
    @staticmethod
    async def fetch_apartment(
        client: ClientSession, *, apartment_id: int
    ) -> schemas.Apartment:
        try:
            async with client.get(
                f"http://search:3000/api/rooms/{apartment_id}"
            ) as response:
                if not response.ok:
                    raise HTTPException(
                        status_code=500, detail="Error while fetching apartment"
                    )
                body = await response.json()
        except aiohttp.ClientConnectorError:
            raise HTTPException(status_code=500, detail="Service unavailable")

        try:
            apartment = schemas.Apartment(**body)
        except ValidationError as e:
            raise HTTPException(
                status_code=500, detail="Get bad response while fetching apartment"
            )

        return apartment
