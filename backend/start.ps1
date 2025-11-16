# Script de démarrage du backend
Write-Host "🚀 Démarrage du backend Immobilier..." -ForegroundColor Green

# Aller à la racine du projet
cd ..

# Activer le venv
Write-Host "📦 Activation du venv..." -ForegroundColor Blue
.\venv\Scripts\activate

# Aller dans le dossier backend
cd backend

# Lancer le serveur
Write-Host "🔧 Lancement du serveur FastAPI..." -ForegroundColor Blue
python main.py
