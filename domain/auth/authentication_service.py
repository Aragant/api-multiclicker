from datetime import datetime, timedelta, timezone
import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from domain.user.user_services import UserServices
from jwt.exceptions import InvalidTokenError
import jwt
from infrastructure.error.error import ForbiddenError
from infrastructure.security.password_hash_service import get_password_hash
from domain.user.user_repository import UserRepository
from domain.user.user_model import User


from domain.user.user_schema import UserForLogin, UserPrivate
from infrastructure.security.password_hash_service import verify_password
from infrastructure.security.token_data import TokenData
from infrastructure.logging.logging_config import logger
from domain.user.user_schema import UserSignUp

ALGORITHM = "HS256"
SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_REFRESH_KEY = os.environ.get("SECRET_REFRESH_KEY")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def authenticate_user(username: str, password: str):
    user: UserForLogin = await UserServices().get_by_username_for_login(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    logger.info("Utilisateur connecté : %s", user.username)
    return user

async def create_user(user_data: UserSignUp):
    existing_user = await UserRepository().get_by_email(user_data.email)
    if existing_user:
        raise ForbiddenError("Un utilisateur avec cet email existe déjà.")

    hashed_pwd = get_password_hash(user_data.password)

    user: UserSignUp = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pwd,
        disabled=False, 
    )

    new_user = await UserRepository().save(user)
    return new_user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = await UserServices().get_by_id(id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserPrivate, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
