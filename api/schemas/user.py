import bcrypt
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    def encrypt_password(self):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), salt)
        self.password = hashed_password.decode("utf-8")


class UserLogin(BaseModel):
    email: EmailStr
    password: str
