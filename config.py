import os

from dotenv import load_dotenv

from utils import generate_jwt_secret_key

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
JWT_SECRET_KEY = generate_jwt_secret_key()

DATABASE_URL = os.getenv("PROD_INTERNAL_DB_URL", "")
