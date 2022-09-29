from sqlalchemy import Column, Integer, String, DateTime

from app.core.db import Base


class BlacklistedToken(Base):
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True)
    token = Column(String)
    expires_at = Column(DateTime)
