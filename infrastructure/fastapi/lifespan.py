from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.database.create_table import create_table
from infrastructure.logging.logging_config import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield
    logger.info("Arrêt de l'application.")
