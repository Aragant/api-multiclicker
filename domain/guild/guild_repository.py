from sqlalchemy import select
from infrastructure.database.base_repository import BaseRepository
from domain.guild.guild_model import Guild
from domain.member.member_model import Member, MemberRole
from sqlalchemy.orm import selectinload
from infrastructure.error.error import ForbiddenError, NotFoundError


class GuildRepository:
    def __init__(self):
        self.repo = BaseRepository(Guild)

    async def get_by_id(self, guild_id: str):
        guild = await self.repo._get(
            id=guild_id, options=[selectinload(Guild.members).selectinload(Member.user)]
        )
        if not guild:
            raise NotFoundError("Guilde")
        return guild

    async def get_all(self):
        return await self.repo._get_all_with_option(
            options=[Guild.members, Member.user]
        )

    async def get_by_master_user_id(self, user_id: str):
        options = [selectinload(Guild.members).selectinload(Member.user)]

        # self.repo._get est inutilisable ici ou je ne sait pas exactement comment
        query = (
            select(Guild)
            .join(Member, Member.guild_id == Guild.id)
            .where(Member.user_id == user_id)
            .options(*options)
        )

        async with self.repo.transaction() as session:
            result = await session.execute(query)
            guild = result.scalars().first()

        if not guild:
            raise NotFoundError("Guilde non trouvée pour l'utilisateur spécifié.")

        return guild

    async def save(self, guild: Guild):
        return await self.repo._save(guild)

    async def get_by_name(self, name: str):
        return await self.repo._get(name=name)

    async def update(self, guild_data: dict):
        guild_instance = self.repo.schema_class(**guild_data)
        return await self.repo._update(guild_instance)

    async def add_member(self, new_member: Member) -> dict:
        """Ajoute un membre à une guilde."""
        saved_member = await self.repo._save(new_member)
        return saved_member
