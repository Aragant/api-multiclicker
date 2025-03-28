from domain.guild.guild_schema import GuildFlat , NewGuild
from domain.guild.guild_model import Guild
from domain.guild.guild_repository import GuildRepository

class GuildDomain:
    async def create(self, newGuild : NewGuild) -> GuildFlat:
        
        guild = Guild(
            name=newGuild.name,
            description=newGuild.description,
            owner_id=newGuild.owner_id,
        )
        
        created_guild = await GuildRepository().save(guild)
        return GuildFlat.model_validate(created_guild)