from contextlib import asynccontextmanager
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from infrastructure.database.database import Base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # Base en mémoire

@pytest_asyncio.fixture(scope="session")
async def engine():
    """Crée un moteur de base de données asynchrone."""
    engine = create_async_engine(DATABASE_URL)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_session(engine):
    """Crée une session asynchrone et réinitialise la base avant chaque test."""
    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


    async with async_session_factory() as session:
        yield session
        await session.rollback()
        



@asynccontextmanager
@pytest_asyncio.fixture(scope="function")
async def transaction(async_session):
    session: AsyncSession = async_session
    try:
        yield session
        await session.rollback()
    except Exception as e:
        await session.rollback()
        print("PRINT", e)
        raise e
    finally:
        await session.close()
