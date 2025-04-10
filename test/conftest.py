import os
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Load test environment variables
load_dotenv('.env.test')

# Import après chargement des variables d'env
from infrastructure.database.database import Base
from infrastructure.database.base_repository import BaseRepository
from fake_model import FakeModel  # à adapter selon ton projet


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Create a test database engine."""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    engine = create_async_engine(DATABASE_URL, echo=True)

    # Création des tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Nettoyage
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def transaction(engine):
    """Create a transaction-scoped session."""
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def async_session(transaction):
    """Alias de transaction pour les tests qui demandent async_session."""
    yield transaction


@pytest_asyncio.fixture
async def repo(transaction):
    """BaseRepository avec session de test."""
    return BaseRepository(FakeModel, lambda: transaction)
