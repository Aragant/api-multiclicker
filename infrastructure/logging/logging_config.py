import os
import logging
from logging.config import dictConfig

# Création du dossier pour les logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/app.log",  # Chemin du fichier de log
            "mode": "a",           # Mode d'écriture : 'a' pour ajouter, 'w' pour écraser
            "encoding": "utf-8",   # Encodage du fichier
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],  # Envoie les logs à la fois dans la console et le fichier
    },
}

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


separator_line = "=" * 30  # Une ligne de 80 caractères
logger.info(separator_line)
logger.info("  Lancement de l'application")
logger.info(separator_line)

