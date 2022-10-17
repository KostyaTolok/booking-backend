from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.payment import BookingCRUD


class BookingServices:
    @staticmethod
    def calculate_price(*, start_date: date, end_date: date, price_per_night: Decimal):
        return (end_date - start_date).days * price_per_night

    @staticmethod
    def check_booking_dates_availability(
        db: Session, *, apartment_id: int, start_date: date, end_date: date
    ):
        date_overlapping_apartments = BookingCRUD.get_date_overlapping(
            db,
            apartment_id=apartment_id,
            start_date=start_date,
            end_date=end_date,
        )

        if date_overlapping_apartments:
            raise HTTPException(status_code=409, detail="Apartments are booked")

    @staticmethod
    def confirm_payment(
        db: Session,
        payment_intent_id: int,
    ):
        payment_intent_db = BookingCRUD.get_by_payment_intent_id(
            db,
            payment_intent_id,
        )

        if not payment_intent_db:
            raise HTTPException(status_code=404)

        BookingCRUD.confirm(
            db,
            payment_intent_db,
        )

    @staticmethod
    def get_users_booked_apartments(
        db: Session,
        user_id: int,
    ):
        return BookingCRUD.get_by_user_id(db, user_id)
