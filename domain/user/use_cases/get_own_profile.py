from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserPrivate
from infrastructure.error.error import NotFoundError
from infrastructure.logging.logging_config import logger

async def get_own_profile(id: str) -> UserPrivate | None:
    user = await UserRepository().get_by_id(id)
    if not user:
        if not user:
            return NotFoundError(message=f"User with id {id} not found")
    logger.info("User found : %s", user)
    return UserPrivate.model_validate(user)
