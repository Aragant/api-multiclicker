from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildWithMembers
from infrastructure.error.error import NotFoundError


async def get_guild_details( guild_id: str) -> GuildWithMembers:
        guild = await GuildRepository().get_by_id(guild_id)
        if not guild:
            raise NotFoundError(message="Guild not found")
        
        
        guild["sum_member"] = len(guild['members'])
        guild["members"] = [member.user.username for member in guild['members']]  
        
        return GuildWithMembers.model_validate(guild)