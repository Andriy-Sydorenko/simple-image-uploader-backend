import os

from dotenv import load_dotenv

from utils import generate_jwt_secret_key

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
JWT_SECRET_KEY = generate_jwt_secret_key()

LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME")
LOCAL_DB_USER = os.getenv("LOCAL_DB_USER")
LOCAL_DB_PASSWORD = os.getenv("LOCAL_DB_PASSWORD")
LOCAL_DB_HOST = os.getenv("LOCAL_DB_HOST")
LOCAL_DB_PORT = os.getenv("LOCAL_DB_PORT")
LOCAL_POSTGRES_SUPERUSER = os.getenv("LOCAL_POSTGRES_SUPERUSER")
LOCAL_POSTGRES_PASSWORD = os.getenv("LOCAL_POSTGRES_PASSWORD")
