import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Load test environment variables
load_dotenv('.env.test')

# Import after environment variables are loaded
from infrastructure.database.database import Base

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
async def session(engine):
    """Create a test database session."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()
