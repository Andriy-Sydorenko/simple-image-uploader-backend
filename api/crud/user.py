from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import User
from api.schemas.user import UserRegister
from api.utils import decode_jwt_token
from engine import get_db


def create_user(user_data: UserRegister) -> User:
    user = User(email=str(user_data.email), hashed_password=user_data.password)
    user.set_password(user_data.password)
    db: Session = next(get_db())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_token(token: str) -> Optional[User]:
    if not token:
        return None
    payload = decode_jwt_token(token)
    user_uuid = payload["user_uuid"]
    try:
        user_uuid = UUID(user_uuid)
    except ValueError:
        return None
    db: Session = next(get_db())
    query = select(User).filter(User.uuid == user_uuid)
    result = db.execute(query)
    user = result.scalars().first()
    return user
