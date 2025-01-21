from infrastructure.logging.logging_config import logger
from infrastructure.database.table.db_modeles import Base
from infrastructure.database.database import engine

def table_create():
  try:
      table_logging()
      Base.metadata.create_all(bind=engine)
      logger.info("Les tables ont été créées avec succès.")
  except Exception as e:
      logger.error("Erreur lors de la création des tables : %s", e)
      raise
    
    
def table_logging():
  if Base.metadata.tables:
      table_names = list(Base.metadata.tables.keys())
      logger.info(f"Tables à créer : {', '.join(table_names)}")