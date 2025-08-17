from domain.guild.guild_repository import GuildRepository
from domain.member.member_schema import MemberApplicant
from infrastructure.error.error import ForbiddenError


async def get_applicants_if_master(user_id: str) -> list[MemberApplicant]:
    repo = GuildRepository()

    guild = await repo.get_by_master_user_id(user_id)

    if not guild:
        raise ForbiddenError("Vous n'êtes pas le maître de cette guilde")

    members = await repo.get_applicants_by_guild_id(guild.id)

    return [
        MemberApplicant(
            id=member.id,                
            username=member.user.username, 
            user_id=member.user_id,
        )
        for member in members
    ]
