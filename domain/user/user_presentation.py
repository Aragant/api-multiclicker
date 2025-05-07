from typing import Annotated
from fastapi import APIRouter, Depends, Query

from domain.auth.authentication_service import get_current_active_user
from domain.user.use_cases import (
    get_own_profile,
    get_profile,
    signup,
    update_profile,
    get_profiles_by_usernames,
)
from domain.user.user_schema import UserPrivate, UserPublic, UserSignUp, UserUpdate

from typing import List

router = APIRouter(prefix="/user", tags=["user"])

def parse_usernames(usernames: str = Query(...)) -> List[str]:
    return [u.strip() for u in usernames.split(",") if u.strip()]

@router.get("", response_model=UserPublic)
async def get_profile_route(id: str):
    return await get_profile(id)


@router.get("/users", response_model=List[UserPublic])
async def get_profiles_route(usernames: List[str] = Depends(parse_usernames)):
    return await get_profiles_by_usernames(usernames)


@router.post("")
async def signup_user_route(user: UserSignUp):
    return await signup(user)


@router.get("/me/", response_model=UserPrivate)
async def get_own_profile_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
):
    return await get_own_profile(current_user.id)


@router.put("/update", response_model=UserPrivate)
async def update_profile_route(
    current_user: Annotated[UserPrivate, Depends(get_current_active_user)],
    user: UserUpdate,
):
    return await update_profile(user, current_user.id)
