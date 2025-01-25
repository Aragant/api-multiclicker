


from contextlib import asynccontextmanager
from infrastructure.database.database import engine
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def transaction():
    session = AsyncSession(bind=engine)
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()