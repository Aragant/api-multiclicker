import os
from typing import TypeVar
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.logging.logging_config import logger

# load_dotenv()



DATABASE_URL: str = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined in the environment")

engine = create_async_engine(DATABASE_URL) #echo=True pour afficher les requetes sql dans les logs

Base = declarative_base()

ConcreteTable = TypeVar("ConcreteTable", bound=Base)

