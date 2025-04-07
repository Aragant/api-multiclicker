from domain.user.user_service import UserService
from domain.user.user_schema import UserSignUp, UserPrivate
from domain.guild.use_cases import create
from domain.guild.guild_schema import GuildCreateRequestBody


async def init_database():
    admin = await create_main_user()
    guild = await create(
        GuildCreateRequestBody(name="guild1", description="admin"), admin.id
    )
    print(f"guild id is {guild.id}")


async def create_main_user() -> UserPrivate:
    user: UserSignUp = UserSignUp(username="admin", password="admin", email="admin")
    return await UserService().create(user)