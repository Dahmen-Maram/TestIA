FROM python:3.10
EXPOSE 10000
# Installer ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
