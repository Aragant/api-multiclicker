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
    guild1 = await create_guild(
        GuildCreateRequestBody(name="guild1", description="admin"), admin.id
    )

    user1 = await create_user("asd")
    guild2 = await create_guild(
        GuildCreateRequestBody(name="guild2", description="guild 2"), user1.id
    )

    user2 = await create_user("te2")
    user3 = await create_user("te")

    await apply_guild(user3.id, guild1.id)
    await apply_guild(user2.id, guild1.id)

    await apply_guild(user3.id, guild2.id)


async def create_main_user() -> UserPrivate:
    user: UserSignUp = User(
        username="admin", password=get_password_hash("admin"), email="admin"
    )
    user = await UserRepository().save(user)
    return UserPrivate.model_validate(user)


async def create_user(all) -> UserPrivate:
    user: UserSignUp = User(
        username=all,
        password=get_password_hash(all),
        email=all,
        description="le meilleur joueur de tous les temps",
    )
    user = await UserRepository().save(user)
    return UserPrivate.model_validate(user)
