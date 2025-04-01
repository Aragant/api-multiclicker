import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from infrastructure.database.database import Base

DATABASE_URL = (
    "sqlite+aiosqlite:///:memory:"  # Base de données en mémoire pour les tests
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def engine():
    """Crée et retourne un moteur de base de données asynchrone."""
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_session(engine):
    """Crée une session asynchrone."""
    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session
        await session.rollback()
