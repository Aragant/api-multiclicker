from sqlalchemy import select
from infrastructure.database.base_repository import BaseRepository
from domain.guild.guild_model import Guild
from domain.member.member_model import Member, MemberRole
from sqlalchemy.orm import selectinload
from infrastructure.database.query_builder import QueryBuilder
from infrastructure.error.error import ForbiddenError, NotFoundError
from domain.user.user_model import User


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
        query = QueryBuilder(Guild).join_relation(Guild.members, Member.user).build()
        return await self.repo._execute_query(query)

    async def get_by_master_user_id(self, user_id: str):
        query = (
            QueryBuilder(Guild)
            .join_relation(Guild.members, Member.user)
            .filter(Member.user_id == user_id)
            .filter(Member.role == MemberRole.MASTER.value)
            .build()
        )
        return await self.repo._execute_one_or_none(query)

    async def get_applicants_by_guild_id(self, guild_id: str) -> list[Member]:
        query = (
            QueryBuilder(Member)
            .filter(Member.guild_id == guild_id)
            .filter(Member.role == MemberRole.APPLICANT.value)
            .join_relation(Member.user, User)
            .build()
        )
        return await self.repo._execute_query(query)

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
