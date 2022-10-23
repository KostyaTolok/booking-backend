from decimal import Decimal

from pydantic.main import BaseModel


class Apartment(BaseModel):
    price: Decimal
