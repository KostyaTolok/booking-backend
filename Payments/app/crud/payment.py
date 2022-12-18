from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy import or_

from app import schemas
from app.core.config import config
from app.models import BookingPayment


class PaymentCRUD:
    @staticmethod
    def get_expired(db) -> List[BookingPayment]:
        payment_expire_timedelta = timedelta(
            minutes=config.PAYMENT_INTENT_EXPIRE_MINUTES
        )
        return (
            db.query(BookingPayment)
            .filter(
                (BookingPayment.succeeded == False)
                & (
                    BookingPayment.created_at
                    < datetime.utcnow() - payment_expire_timedelta
                )
            )
            .all()
        )

    @staticmethod
    def batch_delete(
        db,
        payment_ids: List[int],
    ):
        if payment_ids:
            (
                db.query(BookingPayment)
                .filter(or_(BookingPayment.id == _id for _id in payment_ids))
                .delete(synchronize_session=False)
            )
            db.commit()

    @staticmethod
    def create(
        db,
        payment: schemas.PaymentCreate,
    ) -> BookingPayment:
        payment_db = BookingPayment(**payment.dict())
        db.add(payment_db)
        db.commit()
        db.refresh(payment_db)
        return payment_db

    @staticmethod
    def get_by_payment_intent_id(
        db,
        payment_intent_id: str,
    ) -> BookingPayment:
        return (
            db.query(BookingPayment)
            .filter(BookingPayment.payment_intent_id == payment_intent_id)
            .first()
        )

    @staticmethod
    def confirm(
        db,
        payment_db: BookingPayment,
    ) -> BookingPayment:
        payment_db.succeeded = True
        db.add(payment_db)
        db.commit()
        db.refresh(payment_db)
        return payment_db

    @staticmethod
    def get_date_overlapping(
        db,
        *,
        apartment_id: int,
        start_date: date,
        end_date: date,
    ) -> List[BookingPayment]:
        return (
            db.query(BookingPayment)
            .filter(
                (BookingPayment.apartment_id == apartment_id)
                & (BookingPayment.end_date > start_date)
                & (BookingPayment.start_date < end_date)
            )
            .all()
        )

    @staticmethod
    def get_by_user_id(
        db,
        user_id: int,
    ) -> BookingPayment:
        return db.query(BookingPayment).filter(BookingPayment.user_id == user_id).all()
