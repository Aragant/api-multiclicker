


from contextlib import asynccontextmanager
from infrastructure.database.database import engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async_session = async_sessionmaker(engine, expire_on_commit=False)

@asynccontextmanager
async def transaction():
    session: AsyncSession = async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()