from domain.user.user_model import User
from domain.user.user_repository import UserRepository
from domain.user.user_schema import UserUpdate, UserPrivate
from infrastructure.error.error import NotFoundError
from infrastructure.logging.logging_config import logger

async def update_profile(userData: UserUpdate, id: str) -> UserPrivate:
    
    user = User(id=id, **userData.model_dump(exclude_unset=True))
    user = await UserRepository().update(user)
    logger.info("User updated : %s", user)
    return UserPrivate.model_validate(user)