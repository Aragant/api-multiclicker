from infrastructure.logging.logging_config import logger
from infrastructure.database.models.user_model import Base
from infrastructure.database.database import engine

async def table_create():
  try:
      table_logging()
      
      async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
      
      
      logger.info("Les tables ont été créées avec succès.")
  except Exception as e:
      logger.error("Erreur lors de la création des tables : %s", e)
      raise
    
    
def table_logging():
  if Base.metadata.tables:
      table_names = list(Base.metadata.tables.keys())
      logger.info(f"Tables à créer : {', '.join(table_names)}")