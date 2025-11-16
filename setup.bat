@echo off
REM Script de démarrage du projet Immobilier pour Windows

echo.
echo 🚀 Bienvenue dans le projet Immobilier
echo.
echo Ce script va vous aider à démarrer l'application.
echo.

setlocal enabledelayedexpansion

REM Vérifier si les répertoires existent
if not exist "frontend" (
    echo ❌ Erreur: Le répertoire 'frontend' n'a pas été trouvé
    exit /b 1
)

if not exist "backend" (
    echo ❌ Erreur: Le répertoire 'backend' n'a pas été trouvé
    exit /b 1
)

echo 📦 Installation des dépendances...
echo.

REM Frontend
echo 📝 Frontend:
cd frontend
if not exist "node_modules" (
    echo Installation de npm packages...
    call npm install
)
echo ✅ Frontend prêt
cd ..

echo.

REM Backend
echo 📝 Backend:
cd backend
if not exist "venv" (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

REM Activer venv
call venv\Scripts\activate.bat

REM Vérifier si FastAPI est installé
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installation des packages Python...
    pip install -r requirements.txt
)
echo ✅ Backend prêt
cd ..

echo.
echo 🎯 Prochaines étapes:
echo.
echo 1. Démarrer le BACKEND (ouvrir un nouveau terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 2. Démarrer le FRONTEND (dans un autre terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 3. Ouvrir votre navigateur:
echo    Frontend: http://localhost:5173
echo    API Docs: http://localhost:8000/docs
echo.
pause
