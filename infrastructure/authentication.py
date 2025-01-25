import os
from passlib.context import CryptContext



ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("SECRET_KEY")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)