from domain.guild.guild_schema import GuildFlat, GuildCreateRequestBody, GuildWithMembers
from domain.guild.guild_model import Guild
from domain.member.member_model import Member, MemberRole
from domain.guild.guild_repository import GuildRepository
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class GuildDomain:
    async def create(
        self, newGuild: GuildCreateRequestBody, user_id: str
    ) -> GuildFlat:
        
        try:
            guild = Guild(
                name=newGuild.name,
                description=newGuild.description,
                members=[Member(user_id=user_id, role=MemberRole.MASTER.value)]
            )
            created_guild = await GuildRepository().save(guild)
            return GuildFlat.model_validate(created_guild)
        except IntegrityError as e:
            if "guild_name_key" in str(e.orig):
                raise HTTPException(
                    status_code=409, #conflict
                    detail=f"Une guilde avec le nom '{newGuild.name}' existe déjà."
                )
            raise e
        
    async def get_all(self) -> list[GuildWithMembers]:
        guilds = await GuildRepository().get_all()

        return [
            GuildWithMembers(
                id=guild.id,
                name=guild.name,
                description=guild.description,
                sum_member=len(guild.members) 
            )
            for guild in guilds
        ]