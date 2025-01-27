

from user.user_model import User
from infrastructure.security.authentication import get_password_hash
from user.user_repository import UserRepository
from user.user_schema import UserSignUp


class UserDomain:
    
    async def create(self, user: UserSignUp, provider: str = None):
        if not provider and not user.password:
            raise ValueError("A password should be provided for non SSO registers")
        elif provider and user.password:
            raise ValueError("A password should not be provided for SSO registers")
        
        if user.password:
            password = get_password_hash(user.password)
        else:
            password = None
            
        user = User(
            username=user.username,
            password=password,
            provider=provider
        )
        
        return await UserRepository().save(user)