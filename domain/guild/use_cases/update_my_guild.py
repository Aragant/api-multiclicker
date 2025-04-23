from domain.guild.guild_model import Guild
from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildUpdateRequestBody, GuildFlat
from domain.guild.guild_services import GuildServices
from infrastructure.error.error import ForbiddenError


async def update_my_guild(
    current_user_id: str, updates: GuildUpdateRequestBody
) -> GuildFlat:

    guild = await GuildServices().get_by_master_user_id(current_user_id)

    if not guild:
        raise ForbiddenError("You must be a guild master to update your guild.")

    guild = Guild(id=guild.id, **updates.model_dump(exclude_unset=True))

    updated_guild = await GuildRepository().update(guild)
    return GuildFlat.model_validate(updated_guild)


