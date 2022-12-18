from datetime import timedelta, datetime, date
from typing import List

from sqlalchemy import text

from app import schemas
from app.core.config import config
from app.models import BookingPayment


class PaymentCRUD:
    @staticmethod
    def get_expired(db) -> List[BookingPayment]:
        payment_expire_timedelta = timedelta(
            minutes=config.PAYMENT_INTENT_EXPIRE_MINUTES
        )

        tablename = BookingPayment.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}" 
                  WHERE "{tablename}".succeeded = '{False}'
                  and "{tablename}".created_at < '{datetime.utcnow() - payment_expire_timedelta}'"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().all()

    @staticmethod
    def batch_delete(
        db,
        payment_ids: List[int],
    ):
        if payment_ids:
            tablename = BookingPayment.__tablename__
            filter_params = [f""""{tablename}".id = '{_id}'""" for _id in payment_ids]
            sql = f"""DELETE FROM "{tablename}" 
                      WHERE {' or '.join(filter_params)}"""
            stmt = db.query(BookingPayment).from_statement(text(sql))
            db.execute(stmt)
            db.commit()

    @staticmethod
    def create(
            db,
            payment: schemas.PaymentCreate,
    ) -> BookingPayment:
        obj_in_data = payment.dict(exclude_unset=True)
        tablename = BookingPayment.__tablename__
        cols = [f'"{tablename}".{c} AS {tablename}_{c}'
                for c in BookingPayment.__table__.columns.keys()]
        default_cols = {c.name: c.default.arg({}) if callable(c.default.arg) else c.default.arg
                        for c in BookingPayment.__table__.columns if c.default}
        sql = f"""INSERT INTO "{tablename}" ({", ".join(list(obj_in_data.keys()) + list(default_cols.keys()))}) 
                  VALUES ({", ".join(f"'{v}'" for v in list(obj_in_data.values()) + list(default_cols.values()))})
                  RETURNING {", ".join(cols)}"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one()

    @staticmethod
    def get_by_payment_intent_id(
        db,
        payment_intent_id: str,
    ) -> BookingPayment:
        tablename = BookingPayment.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}"
                  WHERE "{tablename}".payment_intent_id = '{payment_intent_id}'
                  ORDER BY "{tablename}".id desc
                  LIMIT 1"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one_or_none()

    @staticmethod
    def confirm(
        db,
        payment_db: BookingPayment,
    ) -> BookingPayment:
        update_data = schemas.PaymentCreate.from_orm(payment_db)
        update_data = update_data.dict(exclude_unset=True) | {"succeeded": True}
        tablename = BookingPayment.__tablename__
        cols = [f'"{tablename}".{c} AS {tablename}_{c}'
                for c in BookingPayment.__table__.columns.keys()]
        sql = f"""UPDATE "{tablename}" 
                  SET {", ".join(f"{k}='{v}'" for k, v in update_data.items())}
                  WHERE "{tablename}".id = {payment_db.id}
                  RETURNING {", ".join(cols)}"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().one()

    @staticmethod
    def get_date_overlapping(
        db,
        *,
        apartment_id: int,
        start_date: date,
        end_date: date,
    ) -> List[BookingPayment]:
        tablename = BookingPayment.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}" 
                  WHERE "{tablename}".apartment_id = '{apartment_id}'
                  and "{tablename}".end_date > '{end_date}'
                  and "{tablename}".start_date < '{start_date}'"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().all()

    @staticmethod
    def get_by_user_id(
        db,
        user_id: int,
    ) -> List[BookingPayment]:
        tablename = BookingPayment.__tablename__
        sql = f"""SELECT *
                  FROM "{tablename}" 
                  WHERE "{tablename}".user_id = '{user_id}'"""
        stmt = db.query(BookingPayment).from_statement(text(sql))
        result = db.execute(stmt)
        db.commit()
        return result.scalars().all()
