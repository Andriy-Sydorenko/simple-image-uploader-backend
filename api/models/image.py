import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from engine import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    filename = Column(String(64), nullable=False)
    upload_time = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    file_size = Column(Float, nullable=False)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="images")
