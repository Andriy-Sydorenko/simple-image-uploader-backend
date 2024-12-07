import datetime
from typing import Optional

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models.backlisted_token import BlackListedToken
from config import JWT_SECRET_KEY
from engine import get_db


def generate_jwt_token(user_uuid: str) -> str:
    payload = {"user_uuid": user_uuid, "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> dict:
    # TODO: write more precise exception raising and add handling
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("Invalid token")


def extract_jwt_token_from_request(headers: dict) -> Optional[str]:
    auth_header = headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None


def is_blacklisted(auth_token):
    db: Session = next(get_db())
    query = select(BlackListedToken).filter_by(token=auth_token)
    res = db.execute(query).scalars().first()
    return res is not None
