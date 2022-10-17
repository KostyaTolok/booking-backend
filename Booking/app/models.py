from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, DECIMAL

from app.core.db import Base


class Booking(Base):
    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), onupdate=datetime.utcnow)

    succeeded = Column(Boolean, nullable=False, default=False)

    payment_intent_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, nullable=False)

    user_id = Column(Integer, nullable=False)
    apartment_id = Column(Integer, nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    price = Column(DECIMAL, nullable=False)
