from domain.guild.guild_repository import GuildRepository
from domain.guild.guild_schema import GuildWithMembers
from domain.member.member_model import MemberRole


async def get_guild_details( guild_id: str) -> GuildWithMembers:
        guild = await GuildRepository().get_by_id(guild_id)
        if not guild:
            return None
        
        members = [member for member in guild['members'] if member.role != MemberRole.APPLICANT.value]
    

        guild["sum_member"] = len(guild['members'])
        guild["members"] = [member.user.username if member.user else "Unknown User" for member in members]  
        
        return GuildWithMembers.model_validate(guild)
