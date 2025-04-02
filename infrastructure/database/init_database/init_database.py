from domain.user.user_service import UserService
from domain.user.user_schema import UserSignUp


async def init_database():
    await create_main_user()


async def create_main_user():
    user: UserSignUp = UserSignUp(username="admin", password="admin", email="admin")
    await UserService().create(user)
