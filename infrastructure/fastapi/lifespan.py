from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.database.transaction import transaction
from infrastructure.database.create_table import table_create
from infrastructure.logging.logging_config import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    await table_create()
    
    
    
    # add new user to database
    await add_user_to_database()
    
    
    yield
    logger.info("Arrêt de l'application.")


async def add_user_to_database():
    from infrastructure.database.models.user_model import User
    
    async with transaction() as session:
        user = User(username="admin6", password="admin", provider="local")
        session.add(user)
        await session.commit()
        
    async with transaction() as session:
        user = User(username="admin7", password="admin", provider="local")
        session.add(user)
        await session.commit()