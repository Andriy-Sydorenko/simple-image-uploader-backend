from functools import wraps

from robyn import Request, Response

from api.utils import decode_jwt_token


def jwt_required(f):
    @wraps(f)
    def decorated_function(request: Request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(status_code=401, description="Token is missing", headers={})
        try:
            decode_jwt_token(token)
        except Exception as e:
            return Response(status_code=401, description=str(e), headers={})
        return f(request, *args, **kwargs)

    return decorated_function
