from domain.guild.guild_schema import GuildFlat , GuildCreateRequestBody
from domain.guild.guild_model import Guild
from domain.guild.guild_repository import GuildRepository

class GuildDomain:
    async def create(self, newGuild : GuildCreateRequestBody, owner_id: str) -> GuildFlat:
        
        guild = Guild(
            name=newGuild.name,
            description=newGuild.description,
        )
        
        created_guild = await GuildRepository().save(guild)
        return GuildFlat.model_validate(created_guild)