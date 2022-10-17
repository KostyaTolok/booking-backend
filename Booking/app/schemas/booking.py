from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from pydantic.class_validators import validator


class Booking(BaseModel):
    apartment_id: int
    start_date: date
    end_date: date

    @validator("start_date")
    def start_date_gte_today(cls, v):
        if v < date.today():
            raise ValueError("start date must be gather or equal to current date")
        return v

    @validator("end_date")
    def end_date_gt_start_date(cls, v, values, **kwargs):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("end date must be gather to start date")
        return v


class BookingCreate(Booking):
    payment_intent_id: str
    customer_id: str
    user_id: int
    apartment_id: int
    start_date: date
    end_date: date
    price: Decimal


class BookingRetrieve(Booking):
    price: Decimal
