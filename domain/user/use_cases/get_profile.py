from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserPublic
from infrastructure.error.error import NotFoundError
from infrastructure.logging.logging_config import logger

async def get_profile(id: str) -> UserPublic | None:
    user = await UserRepository().get_by_id(id)
    if not user:
        return NotFoundError(message=f"User with id {id} not found")
    logger.info("User found : %s", user)
    return UserPublic.model_validate(user)
