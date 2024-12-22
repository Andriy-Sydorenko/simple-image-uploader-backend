from robyn import Request, Response, Robyn


def ALLOW_CORS(app: Robyn, origins: list[str] | str = "*"):
    if isinstance(origins, str):
        origins = [origins]

    @app.before_request()
    def cors_handler(request: Request):
        if "*" in origins:
            return request

        try:
            origin = request.headers["referer"]
        except KeyError:
            return Response(status_code=403, description="Request origin is unknown, access denied", headers={})

        if origin and origin not in origins:
            return Response(
                status_code=403, description="Request origin not in allowed origins list, access denied", headers={}
            )
        return request

    app.set_response_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS")
    app.set_response_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    app.set_response_header("Access-Control-Allow-Credentials", "true")
