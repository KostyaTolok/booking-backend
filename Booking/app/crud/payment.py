from datetime import timedelta, datetime, date
from typing import List

from sqlalchemy import or_

from app import schemas
from app.core.config import config
from app.models import Booking


class BookingCRUD:
    @staticmethod
    def get_expired(db) -> List[Booking]:
        payment_expire_timedelta = timedelta(
            minutes=config.PAYMENT_INTENT_EXPIRE_MINUTES
        )
        return (
            db.query(Booking)
            .filter(
                (Booking.succeeded == False)
                & (Booking.created_at < datetime.utcnow() - payment_expire_timedelta)
            )
            .all()
        )

    @staticmethod
    def batch_delete(
        db,
        payment_intent_ids: List[int],
    ):
        if payment_intent_ids:
            (
                db.query(Booking)
                .filter(or_(Booking.id == _id for _id in payment_intent_ids))
                .delete(synchronize_session=False)
            )
            db.commit()

    @staticmethod
    def create(
        db,
        payment_intent: schemas.BookingCreate,
    ) -> Booking:
        payment_intent_db = Booking(**payment_intent.dict())
        db.add(payment_intent_db)
        db.commit()
        db.refresh(payment_intent_db)
        return payment_intent_db

    @staticmethod
    def get_by_payment_intent_id(db, payment_intent_id) -> Booking:
        return (
            db.query(Booking)
            .filter(Booking.payment_intent_id == payment_intent_id)
            .first()
        )

    @staticmethod
    def confirm(
        db,
        payment_intent_db: Booking,
    ) -> Booking:
        payment_intent_db.succeeded = True
        db.add(payment_intent_db)
        db.commit()
        db.refresh(payment_intent_db)
        return payment_intent_db

    @staticmethod
    def get_date_overlapping(
        db,
        *,
        apartment_id: int,
        start_date: date,
        end_date: date,
    ) -> List[Booking]:
        return (
            db.query(Booking)
            .filter(
                (Booking.apartment_id == apartment_id)
                & (Booking.end_date > start_date)
                & (Booking.start_date < end_date)
            )
            .all()
        )

    @staticmethod
    def get_by_user_id(
        db,
        user_id: int,
    ) -> Booking:
        return db.query(Booking).filter(Booking.user_id == user_id).all()
