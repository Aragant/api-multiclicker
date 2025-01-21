from infrastructure.logging.logging_config import logger
from infrastructure.database.db_modeles import Base
from infrastructure.database.database import engine

def create_table():
  try:
      log_table()
      Base.metadata.create_all(bind=engine)
      logger.info("Les tables ont été créées avec succès.")
  except Exception as e:
      logger.error("Erreur lors de la création des tables : %s", e)
      raise
    
    
def log_table():
  if Base.metadata.tables:
      table_names = list(Base.metadata.tables.keys())
      logger.info(f"Tables à créer : {', '.join(table_names)}")