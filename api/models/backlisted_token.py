import datetime

from sqlalchemy import Column, DateTime, Integer, String

from engine import Base


class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    token = Column(String(256), nullable=False)
    blacklisted_on = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
