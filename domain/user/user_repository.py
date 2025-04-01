from infrastructure.database.base_repository import BaseRepository
from domain.user.user_model import User


class UserRepository:
    def __init__(self):
        self.repo = BaseRepository(User)

    async def get_by_username(self, username: str):
        return await self.repo._get(username=username, disabled=False)

    async def get_by_username_for_login(self, username: str):
        return await self.repo._get(username=username, disabled=False)

    async def get_by_id(self, id: str):
        return await self.repo._get(id=id, disabled=False)

    async def get_by_email(self, email: str):
        return await self.repo._get(email=email, disabled=False)

    async def save(self, user: User):
        return await self.repo._save(user)

    async def update(self, user: User):
        return await self.repo._update(user)
