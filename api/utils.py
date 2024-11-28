import datetime
from typing import Optional

import jwt

from config import JWT_SECRET_KEY


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
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def extract_jwt_token_from_request(headers: dict) -> Optional[str]:
    auth_header = headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None
