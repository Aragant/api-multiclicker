import pytest
from infrastructure.database.database import Base, engine  # adapte ça à ton projet

from domain.user.user_model import User  # <- modèle User
from domain.guild.guild_model import Guild
from domain.member.member_model import Member


@pytest.fixture(scope="function", autouse=True)
async def create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield