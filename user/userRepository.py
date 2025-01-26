from infrastructure.database.transaction import transaction
from infrastructure.database.baseRepository import BaseRepository
from infrastructure.database.models.user_model import User
from user.userSchema import UserFlat


class UserRepository(BaseRepository):
    schema_class = User
    
    async def get_by_username(self, username: str) -> UserFlat:
        user = await self._get("username", username)
        return UserFlat.model_validate(user)
