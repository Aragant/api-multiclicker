from domain.guild.guild_domain import GuildDomain
from domain.guild.guild_schema import GuildCreateRequestBody
from domain.user.user_domain import UserDomain
from domain.user.user_service import UserService
from domain.user.user_schema import UserSignUp

async def init_database():
    await create_main_user()

async def create_main_user():
    user: UserSignUp = UserSignUp(username="admin", password="admin", email="admin")
    admin = await UserDomain().create(user)
    guild = await GuildDomain().create(
        GuildCreateRequestBody(name="guild1", description="admin"), admin.id
    )
    print(f"guild id is {guild.id}")
    await UserService().create(user)

