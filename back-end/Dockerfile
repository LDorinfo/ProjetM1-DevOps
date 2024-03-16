# Utilisez l'image officielle Python en tant que base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les dépendances Python
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le code Flask dans le conteneur
COPY . .

# Exposez le port sur lequel votre application Flask écoute
EXPOSE 5000

# Commande pour exécuter l'application Flask
CMD ["python", "app.py","--host=0.0.0.0"]
