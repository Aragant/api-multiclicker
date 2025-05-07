from infrastructure.database.base_repository import BaseRepository
from domain.user.user_model import User
from sqlalchemy.future import select
from domain.user.user_schema import UserPrivate
from domain.member.member_model import MemberRole
from infrastructure.database.transaction import transaction
from sqlalchemy.orm import selectinload, with_loader_criteria
from domain.member.member_model import Member
from typing import List


class UserRepository:
    def __init__(self):
        self.repo = BaseRepository(User)
        self.transaction = transaction

    async def get_by_username(self, username: str):
        return await self.repo._get(username=username, disabled=False)

    async def get_by_username_for_login(self, username: str):
        return await self.repo._get(username=username, disabled=False)

    async def get_multiple_by_username(self, usernames: List[str]):
        return await self.repo._get_multiple(username=usernames, disabled=False)

    async def get_by_id(self, id: str) -> UserPrivate | None:
        async with UserRepository().transaction() as session:
            query = (
                select(User)
                .where(User.id == id, User.disabled == False)
                .options(
                    selectinload(User.members),  # chargement relationnel
                    with_loader_criteria(
                        Member, Member.role != MemberRole.APPLICANT.value
                    ),
                )
            )

            result = await session.execute(query)
            user = result.unique().scalars().one_or_none()

            if not user:
                return None

            guild_id = user.members[0].guild_id if user.members else None

            return UserPrivate.model_validate({**user.as_dict, "guild_id": guild_id})

    async def get_by_email(self, email: str):
        return await self.repo._get(email=email, disabled=False)

    async def save(self, user: User):
        return await self.repo._save(user)

    async def update(self, user: User):
        return await self.repo._update(user)
