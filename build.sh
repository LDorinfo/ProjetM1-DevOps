#!/bin/bash

# Installation des dépendances du frontend React
echo "Installing frontend dependencies..."
cd client
npm install

# Construction du frontend React
echo "Building frontend..."
npm run build

# Copie des fichiers construits dans le répertoire statique de Flask
echo "Copying build files to Flask static directory..."
cp -r build/* ../backend/static/

# Retourner au répertoire principal du projet
cd ..

# Installation des dépendances du backend Flask
echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Build complete!"
