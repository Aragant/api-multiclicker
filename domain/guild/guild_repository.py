from infrastructure.database.base_repository import BaseRepository
from domain.guild.guild_model import Guild
from domain.member.member_model import Member
from sqlalchemy.orm import selectinload
from infrastructure.error.error import NotFoundError

class GuildRepository:
    def __init__(self):
        self.repo = BaseRepository(Guild)

    async def get_by_id(self, guild_id: str):
        guild = await self.repo._get(
            id=guild_id,  
            options=[selectinload(Guild.members).selectinload(Member.user)]
        )
        if not guild:
            raise NotFoundError("Guilde")
        return guild

    async def get_all(self):
        return await self.repo._get_all(
            options=[selectinload(Guild.members).selectinload(Member.user)]
        )

    async def save(self, guild: Guild):
        return await self.repo._save(guild)
