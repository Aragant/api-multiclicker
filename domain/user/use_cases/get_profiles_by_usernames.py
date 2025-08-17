from typing import List
from domain.user.user_schema import UserPublic
from domain.user.user_repository import UserRepository

async def get_profiles_by_usernames(usernames: List[str]) -> List[UserPublic]:
    users = await UserRepository().get_multiple_by_username(usernames)
    return [UserPublic(**user) for user in users if user is not None]
