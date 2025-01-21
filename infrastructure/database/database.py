import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infrastructure.logging.logging_config import logger

load_dotenv()



DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    logger.info("Création d'une nouvelle session de base de données.")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Erreur avec la session de base de données : %s", e)
        raise
    finally:
        db.close()
        logger.info("Fermeture de la session de base de données.")