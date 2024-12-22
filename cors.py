from robyn import Robyn


def ALLOW_CORS(app: Robyn):
    app.set_response_header("Access-Control-Allow-Origin", "*")

    app.set_response_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS")
    app.set_response_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    app.set_response_header("Access-Control-Allow-Credentials", "true")
