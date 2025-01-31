from infrastructure.database.base_repository import BaseRepository
from domain.user.user_model import User
from domain.user.user_schema import UserFlat, UserForLogin, UserPrivate


class UserRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(User)
    
    async def get_by_username(self, username: str):
        return await self._get(username=username, disabled=False)
        
    
    async def get_by_username_for_login(self, username: str):
        return  await self._get(username=username, disabled=False)
    
    async def get_by_id(self, id: str):
        return await self._get(id=id, disabled=False)
    
    async def get_by_email(self, email: str):
        return await self._get(email=email, disabled=False)
    
    async def save(self, user: User):
        return await self._save(user)
    
    async def update(self, user: User):
        return await self._update(user)
    
