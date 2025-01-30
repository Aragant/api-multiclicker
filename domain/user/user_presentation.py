
from typing import Annotated
from fastapi import APIRouter, Depends

from domain.auth.authentication_service import get_current_active_user
from domain.user.user_repository import UserRepository
from infrastructure.logging.logging_config import logger
from domain.user.user_schema import UserFlat, UserPrivate, UserSignUp, UserUpdate
from domain.user.user_domain import UserDomain



router = APIRouter(prefix="/user", tags=["user"])

@router.get("")
async def get_user_route(username: str):
    user: UserFlat = await UserDomain().get_by_username(username)
    return user

@router.post("")
async def create_user_route(user: UserSignUp):
    user = await UserDomain().create(user)
    return user

@router.get("/me/", response_model=UserPrivate)
async def get_current_user_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
):
    return current_user

@router.put("/update", response_model=UserPrivate)
async def update_user_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    user: UserUpdate,
):
    user = await UserDomain().update(user, current_user.id)
    return user
