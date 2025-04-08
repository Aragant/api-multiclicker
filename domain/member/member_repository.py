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
