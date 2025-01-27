from domain.user.user_domain import UserDomain
from domain.user.user_schema import UserSignUp


async def init_database():
    await create_main_user()


async def create_main_user():
    user: UserSignUp = UserSignUp(username="admin", password="admin")
    await UserDomain().create(user)