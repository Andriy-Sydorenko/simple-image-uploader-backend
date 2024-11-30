import datetime

from sqlalchemy import Column, DateTime, Integer, String, select
from sqlalchemy.orm import Session

from engine import Base, get_db


class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    token = Column(String(128), nullable=False)
    blacklisted_on = Column(DateTime, default=datetime.datetime.now(datetime.UTC))

    @staticmethod
    def check_blacklist(auth_token):
        db: Session = next(get_db())
        query = select(BlackListedToken).filter_by(token=auth_token)
        res = db.execute(query).scalars().first()
        return res is not None
