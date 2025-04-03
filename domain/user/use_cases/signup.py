from domain.user.user_model import User
from infrastructure.error.error import DuplicateEntryError
from infrastructure.security.password_hash_service import get_password_hash
from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserSignUp, UserPrivate
from infrastructure.logging.logging_config import logger

async def signup(user: UserSignUp, provider: str = None) -> UserPrivate:
    check_sso_password_constraints(user.password, provider)
    await check_unique_email(user.email)

    password = get_password_hash(user.password) if user.password else None

    user = User(
        username=user.username,
        password=password,
        provider=provider,
        email=user.email,
    )
    
    new_user = await UserRepository().save(user)
    
    logger.info("User created : %s", new_user)
    return UserPrivate.model_validate(new_user)


def check_sso_password_constraints(password: str, provider: str):
    if not provider and not password:
        raise ValueError("A password should be provided for non SSO registers")
    elif provider and password:
        raise ValueError("A password should not be provided for SSO registers")
    

async def check_unique_email(email: str):
    user = await UserRepository().get_by_email(email)
    if user:
        raise DuplicateEntryError(f"User with email {email} already exists")