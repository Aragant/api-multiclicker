from fastapi import APIRouter

from infrastructure.error.error import NotFoundError
from user.userRepository import UserRepository


router = APIRouter(prefix="/auth")


@router.get("/")
async def root():
    return await UserRepository().get_by_username("admin")