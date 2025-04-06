from domain.user.user_model import User
from infrastructure.security.password_hash_service import get_password_hash
from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserForLogin, UserPrivate, UserSignUp, UserUpdate
from infrastructure.logging.logging_config import logger


class UserService:
    async def create(self, user: UserSignUp, provider: str = None) -> UserPrivate:
        if not provider and not user.password:
            raise ValueError("A password should be provided for non SSO registers")
        elif provider and user.password:
            raise ValueError("A password should not be provided for SSO registers")

        if user.password:
            password = get_password_hash(user.password)
        else:
            password = None

        user = User(
            username=user.username,
            password=password,
            provider=provider,
            email=user.email,
        )

        new_user = await UserRepository().save(user)  # created user

        logger.info("User created : %s", new_user)
        return UserPrivate.model_validate(new_user)

    async def get_by_username(self, username: str) -> UserPrivate | None:
        user = await UserRepository().get_by_username(username)
        if not user:
            return None
        logger.info("User found : %s", user)
        return UserPrivate.model_validate(user)

    async def get_by_username_for_login(self, username: str) -> UserForLogin | None:
        user = await UserRepository().get_by_username_for_login(username)
        if not user:
            return None

        logger.info("User found : %s", user)
        return UserForLogin.model_validate(user)

    async def get_by_id(self, id: str) -> UserPrivate | None:
        user = await UserRepository().get_by_id(id)
        if not user:
            return None

        logger.info("User found : %s", user)
        return UserPrivate.model_validate(user)

    async def get_by_email(self, email: str) -> UserPrivate | None:
        user = await UserRepository().get_by_email(email)
        if not user:
            return None

        logger.info("User found : %s", user)
        return UserPrivate.model_validate(user)

    async def update(self, userData: UserUpdate, id: str) -> UserPrivate:
        user = User(id=id, **userData.model_dump(exclude_unset=True))
        user = await UserRepository().update(user)
        logger.info("User updated : %s", user)
        return UserPrivate.model_validate(user)
