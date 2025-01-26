


from contextlib import asynccontextmanager
from infrastructure.database.database import engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from infrastructure.error.error import DatabaseError
from infrastructure.logging.logging_config import logger


async_session = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def transaction():
    session: AsyncSession = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        logger.error("Erreur durant la transaction : %s", e)
        raise DatabaseError
    finally:
        await session.close()