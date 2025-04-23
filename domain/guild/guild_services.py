
from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildPublic


class GuildServices:
    async def get_by_name(self, name: str) -> GuildPublic | None:
        guild = await GuildRepository().get_by_name(name)
        return GuildPublic.model_validate(guild) if guild else None
    
    async def get_by_master_user_id(self, user_id: str) -> GuildPublic | None:
        guild = await GuildRepository().get_by_master_user_id(user_id)
        return GuildPublic.model_validate(guild[0]) if guild else None