from sqlalchemy import select
from infrastructure.database.base_repository import BaseRepository
from domain.guild.guild_model import Guild
from domain.member.member_model import Member, MemberRole
from sqlalchemy.orm import selectinload
from infrastructure.database.query_builder import QueryBuilder

class GuildRepository:
    def __init__(self):
        self.repo = BaseRepository(Guild)

    async def get_by_id(self, guild_id: str):
        query = (
            QueryBuilder(Guild)
            .join_relation(
                Guild.members,
                Member,
                filter_condition=QueryBuilder.or_(
                    Member.role == MemberRole.MASTER.value,
                    Member.role == MemberRole.MEMBER.value
                ),
                load_relation=True  # Assure-toi que les membres sont préchargés
            )
            .filter(Guild.id == guild_id)
            .build()
        )
        guild = await self.repo._execute_query(query)
        return guild[0] if guild else None

    async def get_all(self):
        query = (
            QueryBuilder(Guild)
            .join_relation(Guild.members, Member.user)
            .build()
        )
        return await self.repo._execute_query(query)

    async def get_by_master_user_id(self, user_id: str):
        query = (
            QueryBuilder(Guild)
            .join_relation(Guild.members, Member)
            .filter(Member.user_id == user_id)
            .filter(Member.role == MemberRole.MASTER.value)
            .build()
        )
        return await self.repo._execute_query(query)

    async def save(self, guild: Guild):
        return await self.repo._save(guild)

    async def get_by_name(self, name: str):
        return await self.repo._get(name=name)

    async def update(self, guild: Guild):
        return await self.repo._update(guild)

    async def add_member(self, new_member: Member) -> dict:
        return await self.repo._save(new_member)
        
