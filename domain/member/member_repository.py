from infrastructure.database.base_repository import BaseRepository
from domain.member.member_model import Member, MemberRole


class MemberRepository:
    def __init__(self):
        self.repo = BaseRepository(Member)

    async def save(self, member: Member):
        return await self.repo._save(member)

    async def get_active_member_by_user_id(self, user_id: str):
        member = await self.repo._get(
            user_id=user_id, role=[MemberRole.MEMBER.value, MemberRole.MASTER.value]
        )

        if member:
            return member
        else:
            return None

    async def update_user_role_on_guild(
        self, user_id: str, guild_id: str, role: MemberRole
    ):
        member = await self.repo._real_get(user_id=user_id, guild_id=guild_id)
        if not member:
            return None

        member.role = role.value
        return await self.repo._update(member)

    async def delete_applications_except_guild(self, user_id: str, guild_id: str):
        await self.repo._delete_where(user_id=user_id, not__guild_id=guild_id)
