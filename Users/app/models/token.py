from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models import User


class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    jti = Column(String, unique=True, index=True)
    token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    user = relationship("User", cascade="all,delete", backref="tokens")
    blacklist = relationship(
        "BlacklistedToken", cascade="all,delete", backref="token", uselist=False
    )


class BlacklistedToken(Base):
    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey(Token.id), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
