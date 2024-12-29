from typing import Optional

import cloudinary.uploader
from fastapi import (
    Body,
    Depends,
    FastAPI,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.openapi.models import License
from pydantic import AnyUrl
from sqlalchemy.orm import Session

import config
from api.crud.image import create_image, get_image_by_uuid, get_images_by_user_id
from api.crud.token import add_token_to_blacklisted
from api.crud.user import create_user, get_user_by_email, get_user_by_token
from api.schemas.image import ImageUploadResponseSchema
from api.schemas.user import UserLogin, UserRegister
from api.utils import extract_jwt_token_from_request, generate_jwt_token
from decorators import jwt_required
from engine import get_db
from exceptions import UserAlreadyExistsError, ValidationError
from utils import convert_bytes_to_mb

app = FastAPI(
    title="Image Uploader API",
    description="This is a documentation to an image uploader API.",
    version="1.0.0",
    license_info=License(
        name="BSD2.0",
        url=AnyUrl("https://opensource.org/license/bsd-2-clause"),
    ),
)

cloudinary.config(
    cloud_name=config.CLOUDINARY_CLOUD_NAME,
    api_key=config.CLOUDINARY_API_KEY,
    api_secret=config.CLOUDINARY_API_SECRET,
)


@app.get("/")
def health_check():
    return {"message": "API is running!"}


@app.post("/register/")
def register(register_data: UserRegister = Body(...), db: Session = Depends(get_db)):
    try:
        create_user(register_data, db)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return {"message": "User created successfully"}


@app.post("/login/")
def login(login_data: UserLogin = Body(...), db: Session = Depends(get_db)):
    user = get_user_by_email(str(login_data.email), db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials provided")
    if user.check_password(login_data.password):
        token = generate_jwt_token(str(user.uuid))
        return {
            "user_email": user.email,
            "user_uuid": user.uuid,
            "token": token,
        }
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


@app.post("/logout/")
@jwt_required
def logout(request: Request, db: Session = Depends(get_db)):
    token = extract_jwt_token_from_request(request.headers)
    add_token_to_blacklisted(token, db)
    return Response(
        status_code=status.HTTP_200_OK,
        content="Logged out successfully",
    )


@app.post("/upload/")
def upload_image(request: Request, file: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided",
        )
    file_size = convert_bytes_to_mb(file.size)
    if file_size > 2.0:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 2 MB limit",
        )

    token = extract_jwt_token_from_request(request.headers)
    try:
        user = get_user_by_token(token, db)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    result = cloudinary.uploader.upload(file.file)
    image_url = result["secure_url"]
    image = create_image(file.filename, file_size, image_url, user, db)

    return ImageUploadResponseSchema(
        image_uuid=image.uuid,
        image_url=image.url,
        filename=image.filename,
        file_size=image.file_size,
        upload_time=image.upload_time.isoformat(),
    )


@app.get("/image-preview/{image_uuid}")
def preview_image(request: Request, db: Session = Depends(get_db)):
    image_uuid = request.path_params["image_uuid"]
    image = get_image_by_uuid(image_uuid, db)
    if not image:
        raise HTTPException(
            status_code=400,
            detail="Image not found",
        )
    return {
        "image_url": image.url,
        "filename": image.filename,
        "file_size": image.file_size,
        "upload_time": image.upload_time.isoformat(),
    }


@app.get("/images/")
@jwt_required
def list_images(request: Request, db: Session = Depends(get_db)):
    token = extract_jwt_token_from_request(request.headers)
    try:
        user = get_user_by_token(token, db)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    images = get_images_by_user_id(user.id, db)
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
