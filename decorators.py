from functools import wraps

from robyn import Response

from api.utils import extract_jwt_token_from_request, is_blacklisted


def jwt_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = extract_jwt_token_from_request(request.headers)
        if not token:
            return Response(
                status_code=401,
                description="Token is required",
                headers={},
            )
        if is_blacklisted(token):
            return Response(
                status_code=401,
                description="Token is blacklisted",
                headers={},
            )
        return func(request, *args, **kwargs)

    return wrapper
