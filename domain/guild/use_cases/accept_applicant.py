# domain/guild/use_cases/join_guild.py

from domain.guild.guild_repository import GuildRepository
from domain.member.member_model import Member, MemberRole
from domain.member.member_repository import MemberRepository
from infrastructure.error.error import ForbiddenError


async def accept_applicant(user_id: str, applicant_id: str):
    guild_repo = GuildRepository()
    member_repo = MemberRepository()
    guild = await guild_repo.get_by_master_user_id(user_id)

    if not guild:
        raise ForbiddenError("Vous n'êtes pas le maître de cette guilde")

    await member_repo.update_user_role_on_guild(
        applicant_id, guild.id, MemberRole.MEMBER
    )
    await member_repo.delete_applications_except_guild(applicant_id, guild.id)
    return "true"
