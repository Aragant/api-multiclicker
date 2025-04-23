from domain.user.user_services import UserServices
from domain.user.user_schema import UserSignUp, UserPrivate
from domain.guild.use_cases import create_guild
from domain.guild.guild_schema import GuildCreateRequestBody


async def init_database():
    await create_user("chris")
    await create_user("duo")
    admin = await create_main_user()

    guild = await create_guild(
        GuildCreateRequestBody(name="guild1", description="admin"), admin.id
    )


async def create_main_user() -> UserPrivate:
    user: UserSignUp = UserSignUp(username="admin", password="admin", email="admin")
    return await UserServices().create(user)


async def create_user(duo: str) -> UserPrivate:
    user: UserSignUp = UserSignUp(username=duo, password=duo, email=duo)
    return await UserServices().create(user)
