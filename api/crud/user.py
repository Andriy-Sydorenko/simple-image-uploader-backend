from typing import Optional
from uuid import UUID

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import User
from api.schemas.user import UserRegister
from api.utils import decode_jwt
from exceptions import UserAlreadyExistsError, ValidationError


def create_user(user_data: UserRegister, db: Session) -> User:
    query = select(User).filter(User.email == user_data.email)
    result = db.execute(query)
    existing_user = result.scalars().first()
    if existing_user:
        raise UserAlreadyExistsError("User with this email already exists.")

    user = User(email=str(user_data.email))
    user.set_password(user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_token(token: str, db: Session) -> Optional[User]:
    if not token:
        return None
    try:
        user_uuid = decode_jwt(token)
        user_uuid = UUID(user_uuid)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as exc:
        raise ValidationError(str(exc))
    except ValueError:
        return None
    query = select(User).filter(User.uuid == user_uuid)
    result = db.execute(query)
    user = result.scalars().first()
    return user


def get_user_by_email(email: str, db: Session) -> Optional[User]:
    query = select(User).filter(User.email == email)
    result = db.execute(query)
    user = result.scalars().first()
    return user
