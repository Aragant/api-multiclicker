from domain.guild.guild_schema import (
    GuildFlat,
    GuildCreateRequestBody,
    GuildWithSumMembers,
    GuildWithMembers
)
from domain.guild.guild_model import Guild
from domain.member.member_model import Member, MemberRole
from domain.guild.guild_repository import GuildRepository
from sqlalchemy.exc import IntegrityError
from infrastructure.error.error import ConflictError


class GuildDomain:
    async def create(self, newGuild: GuildCreateRequestBody, user_id: str) -> GuildFlat:
        try:
            guild = Guild(
                name=newGuild.name,
                description=newGuild.description,
                members=[Member(user_id=user_id, role=MemberRole.MASTER.value)],
            )
            created_guild = await GuildRepository().save(guild)
            return GuildFlat.model_validate(created_guild)
        except IntegrityError as e:
            if "guild_name_key" in str(e.orig):
                raise ConflictError(f"Une guilde avec le nom '{newGuild.name}' existe déjà.")
            raise e

    async def get_all(self) -> list[GuildWithSumMembers]:
        guilds = await GuildRepository().get_all()

        def setGuildMemberLength(guild):
            guild["sum_member"] = len(guild['members'])
            return GuildWithSumMembers.model_validate(guild)

        guildsWithMemberLength = map(
            setGuildMemberLength,
            guilds,
        )
        
        return guildsWithMemberLength
    
    async def get_by_id(self, guild_id: str) -> GuildWithMembers:
        guild = await GuildRepository().get_by_id(guild_id)
        if not guild:
            return None
        
        guild["sum_member"] = len(guild['members'])
        guild["members"] = [member.user.username for member in guild['members']]  
        
        return GuildWithMembers.model_validate(guild)
