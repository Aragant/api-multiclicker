from domain.user.user_model import User
from domain.user.user_repository import UserRepository
from domain.user.user_services import UserServices
from domain.user.user_schema import UserSignUp, UserPrivate
from domain.guild.use_cases import create_guild
from domain.guild.guild_schema import GuildCreateRequestBody
from infrastructure.security.password_hash_service import get_password_hash
from domain.guild.use_cases import apply_guild

async def init_database():
    admin = await create_main_user()
    guild = await create_guild(
        GuildCreateRequestBody(name="guild1", description="admin"), admin.id
    )
    user = await create_seconde_user()
    await apply_guild(user.id, guild.id)



async def create_main_user() -> UserPrivate:
    user: UserSignUp = User(username="admin", password=get_password_hash("admin"), email="admin")
    user = await UserRepository().save(user)
    return UserPrivate.model_validate(user)

async def create_seconde_user() -> UserPrivate:
    user: UserSignUp = User(username="te", password=get_password_hash("te"), email="te")
    user = await UserRepository().save(user)
    return UserPrivate.model_validate(user)