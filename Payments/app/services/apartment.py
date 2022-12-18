import logging
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientSession
from fastapi import HTTPException, status
from pydantic.error_wrappers import ValidationError

from app import schemas
from app.core.config import config


class ApartmentServices:
    @staticmethod
    async def fetch_apartment(
        client: ClientSession,
        *,
        apartment_id: int,
    ) -> schemas.Apartment:
        try:
            async with client.get(
                urljoin(config.SEARCH_SERVICE_API_URL, f"rooms/{apartment_id}" + "/")
            ) as response:
                if response.status == status.HTTP_404_NOT_FOUND:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Apartment not found",
                    )
                if not response.ok:
                    logging.error(
                        f"Apartment {apartment_id} fetching failed. {response.json()}. {response.url}"
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Error while fetching apartment",
                    )
                body = await response.json()
        except aiohttp.ClientConnectorError:
            logging.error(
                f"Client connector error. Connection to search service failed."
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Search service unavailable",
            )

        try:
            apartment = schemas.Apartment(**body)
        except ValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Get bad response while fetching apartment",
            )

        return apartment
