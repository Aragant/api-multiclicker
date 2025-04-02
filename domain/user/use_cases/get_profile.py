from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserPublic
from infrastructure.logging.logging_config import logger

async def get_profile(id: str) -> UserPublic | None:
    user = await UserRepository().get_by_id(id)
    if not user:
        return None
    logger.info("User found : %s", user)
    return UserPublic.model_validate(user)
