from uuid import UUID

import cloudinary.uploader
from robyn import OpenAPI, Request, Response, Robyn
from robyn.openapi import Components, License, OpenAPIInfo
from sqlalchemy import select
from sqlalchemy.orm import Session

import config
from api.crud.user import create_user, get_user_by_token
from api.models import Image, User
from api.models.backlisted_token import BlackListedToken
from api.schemas.user import UserLogin, UserRegister
from api.utils import extract_jwt_token_from_request, generate_jwt_token
from cors import ALLOW_CORS
from decorators import jwt_required
from engine import get_db
from exceptions import UserAlreadyExistsError, ValidationError
from utils import ALLOWED_METHODS, convert_bytes_to_mb

app = Robyn(
    file_object=__file__,
    openapi=OpenAPI(
        info=OpenAPIInfo(
            title="Image Uploader API",
            description="This is a documentation to a image uploader API.",
            version="1.0.0",
            license=License(
                name="BSD2.0",
                url="https://opensource.org/license/bsd-2-clause",
            ),
            components=Components(),
        ),
    ),
)
ALLOW_CORS(app)
cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
)


@app.get("/")
def index():
    return "Hello World!"


@app.post("/register/")
def register(request):
    try:
        user_data = UserRegister(**request.json())
    except ValueError:
        return Response(status_code=400, description="Incorrect credentials provided", headers={})
    try:
        create_user(user_data)
    except UserAlreadyExistsError as exc:
        return Response(status_code=400, description=str(exc), headers={})
    return {"message": "User created successfully"}


@app.post("/login/")
def login(request):
    try:
        login_data = UserLogin(**request.json())
    except ValueError:
        return Response(status_code=400, description="Incorrect credentials provided", headers={})
    db: Session = next(get_db())
    query = select(User).filter(User.email == login_data.email)
    result = db.execute(query)
    user = result.scalars().first()
    if user and user.check_password(login_data.password):
        token = generate_jwt_token(str(user.uuid))
        return {
            "user_email": user.email,
            "user_uuid": user.uuid,
            "token": token,
        }
    return Response(status_code=400, description="Invalid credentials", headers={})


@app.post("/logout/")
@jwt_required
def logout(request):
    token = extract_jwt_token_from_request(request.headers)
    db: Session = next(get_db())
    blacklisted_token = BlackListedToken(token=token)
    db.add(blacklisted_token)
    db.commit()
    return Response(
        status_code=200,
        description="Logged out successfully",
        headers={},
    )


@app.post("/upload/")
def upload_image(request):
    try:
        file_name, byted_file = list(request.files.items())[-1]
    except IndexError:
        return Response(
            status_code=400,
            description="No file provided",
            headers={},
        )

    if convert_bytes_to_mb(len(byted_file)) > 2.0:
        return Response(
            status_code=400,
            description="File size exceeds 2 MB limit",
            headers={},
        )

    token = extract_jwt_token_from_request(request.headers)
    try:
        user = get_user_by_token(token)
    except ValidationError as exc:
        return Response(status_code=400, description=str(exc), headers={})
    db: Session = next(get_db())
    result = cloudinary.uploader.upload(byted_file)
    image_url = result["secure_url"]
    file_size = convert_bytes_to_mb(result["bytes"])
    image = Image(filename=file_name, file_size=file_size, url=image_url)
    if user:
        image.user_id = user.id
    db.add(image)
    db.commit()
    db.refresh(image)
    return {
        "image_uuid": image.uuid,
        "image_url": image.url,
        "filename": image.filename,
        "file_size": image.file_size,
        "upload_time": image.upload_time.isoformat(),
    }


@app.get("/image-preview/:image_uuid")
def preview_image(request):
    image_uuid = request.path_params["image_uuid"]
    db: Session = next(get_db())
    query = select(Image).filter(Image.uuid == UUID(image_uuid))
    result = db.execute(query)
    image = result.scalars().first()
    if not image:
        return Response(
            status_code=400,
            description="Image not found",
            headers={},
        )
    return {
        "image_url": image.url,
        "filename": image.filename,
        "file_size": image.file_size,
        "upload_time": image.upload_time.isoformat(),
    }


@app.get("/images/")
@jwt_required
def list_images(request):
    db: Session = next(get_db())
    token = extract_jwt_token_from_request(request.headers)
    try:
        user = get_user_by_token(token)
    except ValidationError as exc:
        return Response(status_code=400, description=str(exc), headers={})

    query = select(Image).filter(Image.user_id == user.id)
    result = db.execute(query)
    images = result.scalars().all()
    return {
        "images": [
            {
                "image_uuid": image.uuid,
                "image_url": image.url,
                "filename": image.filename,
                "file_size": image.file_size,
                "upload_time": image.upload_time.isoformat(),
            }
            for image in images
        ]
    }


@app.before_request()
def handle_unsupported_methods(request: Request):
    request_path = request.url.path.rstrip("/")
    for path in ALLOWED_METHODS:
        if path != "/" and request_path.startswith(path.rstrip("/")):
            if request.method not in ALLOWED_METHODS[path]:
                return Response(status_code=405, description="Method Not Allowed", headers={})
            break
        elif path == "/" and request_path == "":
            if request.method not in ALLOWED_METHODS[path]:
                return Response(status_code=405, description="Method Not Allowed", headers={})
            break
    else:
        return Response(status_code=404, description="Not Found", headers={})
    return request


if __name__ == "__main__":
    app.start(host="0.0.0.0", port=8080)
