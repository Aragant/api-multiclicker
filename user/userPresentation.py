
from fastapi import APIRouter

from user.userRepository import UserRepository


router = APIRouter(prefix="/user")

@router.get("")
async def get_user(username: str):
    return await UserRepository().get_by_username(username)