import uuid

import bcrypt
from sqlalchemy import UUID, Boolean, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)

    email = Column(String(64), nullable=False, unique=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    hashed_password = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)

    images = relationship("Image", back_populates="user")

    UniqueConstraint("email", name="uq_user_email")

    def __repr__(self):
        return "<User {email!r}>".format(email=self.email)

    def set_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password.encode("utf-8"))
