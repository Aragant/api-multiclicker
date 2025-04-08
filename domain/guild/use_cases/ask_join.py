# domain/guild/use_cases/join_guild.py

from domain.guild.guild_repository import GuildRepository
from domain.member.member_model import Member, MemberRole
from domain.member.member_repository import MemberRepository
from infrastructure.error.error import ForbiddenError


async def ask_join(user_id: str, guild_id: str):
    repo = GuildRepository()

    # check user already in a guild
    existing_member = await MemberRepository().get_active_member_by_user_id(user_id)
    if existing_member:
        raise ForbiddenError("Vous ne pouvez pas rejoindre cette guilde.")

    # create member instance
    member = Member(user_id=user_id, guild_id=guild_id, role=MemberRole.APPLICANT.value)

    # asking to join
    new_member = await repo.add_member(member)
    if not new_member:
        raise ForbiddenError("Impossible de rejoindre la guilde.")

    return new_member
