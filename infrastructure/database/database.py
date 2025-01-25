import os
from typing import TypeVar
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.logging.logging_config import logger

# load_dotenv()



DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

ConcreteTable = TypeVar("ConcreteTable", bound=Base)

