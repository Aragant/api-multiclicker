


from contextlib import asynccontextmanager
from infrastructure.database.database import async_session


@asynccontextmanager
async def transaction():
    session = async_session()
    
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()