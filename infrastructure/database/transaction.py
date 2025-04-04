from contextlib import asynccontextmanager
from infrastructure.database.database import engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from infrastructure.logging.logging_config import logger
import inspect


async_session = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def transaction(custom_session=None, commit=True):
    session: AsyncSession = custom_session or async_session()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        database_error_logger(e)
        raise e
    finally:
        await session.close()


def database_error_logger(e):
    frame = inspect.stack()[3]
    caller_function = frame.function
    caller_class = frame.frame.f_locals["self"].__class__.__name__
    logger.error(
        "Error during transaction in '%s' method of '%s' class : %s",
        caller_function,
        caller_class,
        e,
    )
