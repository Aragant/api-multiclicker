import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

if "pytest" in sys.modules:
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:  
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined in the environment")

engine = create_async_engine(
    DATABASE_URL
)  # echo=True pour afficher les requetes sql dans les logs

Base = declarative_base()
