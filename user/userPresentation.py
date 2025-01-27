
from fastapi import APIRouter

from user.userRepository import UserRepository
from infrastructure.logging.logging_config import logger
from user.userSchema import UserFlat, UserSignUp
from user.user_domain import UserDomain



router = APIRouter(prefix="/user", tags=["user"])

@router.get("")
async def get_user(username: str):
    user: UserFlat =  await UserRepository().get_by_username(username)
    logger.info("Utilisateur trouvé : %s", user)
    return user

@router.post("")
async def create_user(user: UserSignUp):
    user = await UserDomain().create(user)
    return user