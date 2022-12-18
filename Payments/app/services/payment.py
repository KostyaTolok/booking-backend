import logging
from datetime import date
from decimal import Decimal

from aiohttp import ClientSession
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.payment import PaymentCRUD
from app.events import send_payment_event
from app.lambdas import invoke_collect_bookings


class PaymentServices:
    @staticmethod
    def calculate_price(
        *,
        start_date: date,
        end_date: date,
        price_per_night: Decimal,
    ):
        return (end_date - start_date).days * price_per_night

    @staticmethod
    def check_booking_dates_availability(
        db: Session,
        *,
        apartment_id: int,
        start_date: date,
        end_date: date,
    ):
        date_overlapping_apartments = PaymentCRUD.get_date_overlapping(
            db,
            apartment_id=apartment_id,
            start_date=start_date,
            end_date=end_date,
        )

        if date_overlapping_apartments:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Apartments are booked",
            )

    @staticmethod
    async def confirm_payment(
        db: Session,
        client: ClientSession,
        payment_intent_id: str,
    ):
        payment_db = PaymentCRUD.get_by_payment_intent_id(
            db,
            payment_intent_id,
        )

        if not payment_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        payment_db = PaymentCRUD.confirm(
            db,
            payment_db,
        )

        message = {
            "message": "payment confirmed successfully",
            "user_id": payment_db.user_id,
            "apartment_id": payment_db.apartment_id,
            "start_date": payment_db.start_date,
            "end_date": payment_db.end_date,
            "succeeded_at": payment_db.updated_at,
            "price": payment_db.price,
        }
        await send_payment_event(message)
        await invoke_collect_bookings(
            client,
            user_id=payment_db.user_id,
            apartment_id=payment_db.apartment_id,
            start_date=payment_db.start_date,
            end_date=payment_db.end_date,
        )

        logging.info(
            f"Payment {payment_db.payment_intent_id} confirmed successfully. {message}"
        )

    @staticmethod
    def get_users_booked_apartments(
        db: Session,
        user_id: int,
    ):
        return PaymentCRUD.get_by_user_id(db, user_id)

    @staticmethod
    def create_payment(
        db: Session,
        payment: schemas.PaymentCreate,
    ) -> models.BookingPayment:
        return PaymentCRUD.create(db, payment)
