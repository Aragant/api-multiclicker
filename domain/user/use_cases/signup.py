from domain.user.user_model import User
from infrastructure.security.password_hash_service import get_password_hash
from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserSignUp, UserPrivate
from infrastructure.logging.logging_config import logger

async def signup(user: UserSignUp, provider: str = None) -> UserPrivate:
    if not provider and not user.password:
        raise ValueError("A password should be provided for non SSO registers")
    elif provider and user.password:
        raise ValueError("A password should not be provided for SSO registers")

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
