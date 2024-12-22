from dotenv import load_dotenv

from utils import EnvParser, generate_jwt_secret_key

env = EnvParser()

load_dotenv()

CLOUDINARY_CLOUD_NAME = env.str("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = env.str("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = env.str("CLOUDINARY_API_SECRET")
JWT_SECRET_KEY = generate_jwt_secret_key()

DEPLOY = env.bool("DEPLOY", False)
DATABASE_URL = env.str("PROD_INTERNAL_DB_URL", "") if DEPLOY else env.str("PROD_EXTERNAL_DB_URL", "")
ALLOWED_ORIGINS = env.list("ALLOWED_ORIGINS", [])
