from infrastructure.database.base_repository import BaseRepository
from domain.user.user_model import User
from domain.user.user_schema import UserFlat, UserForLogin, UserPrivate


class UserRepository(BaseRepository):
    schema_class = User
    
    async def get_by_username(self, username: str) -> UserFlat:
        user = await self._get("username", username)
        return UserFlat.model_validate(user)
    
    async def get_by_username_for_login(self, username: str) -> UserForLogin:
        user = await self._get("username", username)
        return UserForLogin.model_validate(user)
    
    async def save(self, user: User) -> UserPrivate:
        user = await self._save(user)
        return UserPrivate.model_validate(user)
    
