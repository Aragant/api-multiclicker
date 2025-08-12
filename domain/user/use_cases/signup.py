import re

from domain.user.user_model import User
from infrastructure.error.error import DuplicateEntryError, UnprocessableEntityError
from infrastructure.security.password_hash_service import get_password_hash
from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserSignUp, UserPrivate
from infrastructure.logging.logging_config import logger

async def signup(user: UserSignUp) -> UserPrivate:
    
    await check_unique_email(user.email)
    
    await check_unique_username(user.username)
    
    if not is_valid_password(user.password):
        raise UnprocessableEntityError("password", "Password must have at least 8 characters and contain at least one uppercase letter, one lowercase letter and one digit.")

    password = get_password_hash(user.password)

    user = User(
        username=user.username,
        password=password,
        email=user.email,
    )
    
    new_user = await UserRepository().save(user)
    
    logger.info("User created : %s", new_user)
    return UserPrivate.model_validate(new_user)

async def check_unique_email(email: str):
    user = await UserRepository().get_by_email(email)
    if user:
        raise DuplicateEntryError("email_exists", f"User with email {email} already exists")
    

async def check_unique_username(username: str):
    user = await UserRepository().get_by_username(username)
    if user:
        raise DuplicateEntryError("username_exists", f"User with username {username} already exists")
    
def is_valid_password(password: str) -> bool:
    if len(password) <= 8:
        return False
    if not re.search(r"[A-Z]", password):  # au moins une majuscule
        return False
    if not re.search(r"[a-z]", password):  # au moins une minuscule
        return False
    if not re.search(r"[0-9]", password):  # au moins un chiffre
        return False
    return True