
from fastapi import APIRouter

from user.userRepository import UserRepository
from infrastructure.logging.logging_config import logger
from user.userSchema import UserFlat



router = APIRouter(prefix="/user")

@router.get("")
async def get_user(username: str):
    user: UserFlat =  await UserRepository().get_by_username(username)
    logger.info("Utilisateur trouvé : %s", user)
    return user