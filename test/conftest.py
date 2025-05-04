import os
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager

# Load test environment variables from .env.test
load_dotenv('.env.test')

# After env loaded, import the database models
from infrastructure.database.database import Base
from domain.user.user_model import User
from domain.member.member_model import Member
from domain.guild.guild_model import Guild

# Récupère l'URL de la DB de test
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

# Crée l'engine une seule fois pour tous les tests
@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    # Création des tables (pour les tests simples qui ne recréent pas tout à chaque fois)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup final
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

# Session asynchrone simple (sans recréation de la DB à chaque test)
@pytest_asyncio.fixture
async def session(engine):
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

# Même que "session", mais nom plus explicite pour tests async
@pytest_asyncio.fixture
async def async_session(session):
    yield session  # alias, pour compatibilité

# Transaction complète avec DROP/CREATE à chaque test
@pytest_asyncio.fixture(scope="function")
async def transaction(engine):
    # Réinitialise la base pour un test complètement isolé
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()
