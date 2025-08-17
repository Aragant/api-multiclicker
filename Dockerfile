# Utilise une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Exposer le port d'écoute
EXPOSE 8000

# Lancer l'application (FastAPI via Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
