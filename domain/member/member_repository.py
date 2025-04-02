from infrastructure.database.base_repository import BaseRepository
from domain.member.member_model import Member


class MemberRepository:
    def __init__(self):
        self.repo = BaseRepository(Member)

    async def save(self, member: Member):
        return await self.repo._save(member)