from functools import wraps

from fastapi import HTTPException

from api.utils import extract_jwt_token_from_request, is_blacklisted


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = extract_jwt_token_from_request(request.headers)
        if not token:
            return HTTPException(
                status_code=401,
                detail="Token is required",
            )
        if is_blacklisted(token):
            return HTTPException(
                status_code=401,
                detail="Token is blacklisted",
            )
        return func(request, *args, **kwargs)

    return wrapper
