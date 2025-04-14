from sqlite3 import IntegrityError as SQLiteIntegrityError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from domain.guild.guild_model import Guild
from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildCreateRequestBody, GuildFlat
from domain.guild.guild_services import GuildServices
from domain.member.member_model import Member, MemberRole
from infrastructure.error.error import ConflictError, DuplicateEntryError


async def create_guild(newGuild: GuildCreateRequestBody, user_id: str) -> GuildFlat:
    
    if await GuildServices().get_by_name(newGuild.name):
        raise DuplicateEntryError(f"Guild with name {newGuild.name} already exists")
    
    guild = Guild(
        name=newGuild.name,
        description=newGuild.description,
        members=[Member(user_id=user_id, role=MemberRole.MASTER.value)],
    )
    created_guild = await GuildRepository().save(guild)
    return GuildFlat.model_validate(created_guild)