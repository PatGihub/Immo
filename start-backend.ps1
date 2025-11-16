# Script de demarrage rapide du backend

Write-Host "Demarrage du Backend..." -ForegroundColor Green

# Activer le venv
& .\venv\Scripts\Activate.ps1

# Aller au dossier backend
cd backend

# Lancer le serveur
Write-Host "Serveur FastAPI en cours de demarrage..." -ForegroundColor Blue
python main.py
