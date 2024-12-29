import datetime
from typing import Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.datastructures import Headers

from api.models.backlisted_token import BlackListedToken
from config import JWT_ENCRYPTION_ALGORITHM, JWT_SECRET_KEY
from engine import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenData(BaseModel):
    user_uuid: Optional[str] = None


def generate_jwt_token(user_uuid: str) -> str:
    payload = {
        "user_uuid": user_uuid,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ENCRYPTION_ALGORITHM])
        user_uuid: str = payload["user_uuid"]
        return user_uuid
    except (KeyError, ValueError):
        raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def is_blacklisted(auth_token):
    db: Session = next(get_db())
    query = select(BlackListedToken).filter_by(token=auth_token)
    res = db.execute(query).scalars().first()
    return res is not None


def extract_jwt_token_from_request(headers: Headers) -> Optional[str]:
    auth_header = headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None
