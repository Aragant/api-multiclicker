import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager

# Load test environment variables
load_dotenv('.env.test')

# Import after environment variables are loaded
from infrastructure.database.database import Base
from domain.user.user_model import User
from domain.member.member_model import Member
from domain.guild.guild_model import Guild

@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create a test database engine."""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def async_session(engine):
    """Create a test database session."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope="function")
async def transaction(engine, async_session):
    """Create a test database transaction."""
    # Drop and recreate tables for each test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session.begin():
        yield async_session
        await async_session.rollback() 