from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.database.init_database.init_database import init_database
from infrastructure.database.transaction import transaction
from infrastructure.database.create_table import table_create
from infrastructure.logging.logging_config import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    await table_create()    
    await init_database()
    yield
    logger.info("Arrêt de l'application.")

