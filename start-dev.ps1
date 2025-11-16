# Script de demarrage complet pour le projet Immobilier

Write-Host "Demarrage du projet Immobilier..." -ForegroundColor Green
Write-Host ""

# Activer le venv
Write-Host "Activation du venv..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "venv active!" -ForegroundColor Green
Write-Host ""
Write-Host "Lancement du BACKEND..." -ForegroundColor Cyan
Write-Host "Les serveurs tourneront sur :" -ForegroundColor Yellow
Write-Host "  Backend:  http://localhost:8000"
Write-Host "  Frontend: http://localhost:5173 (lance-le dans un autre terminal avec: cd frontend; npm run dev)"
Write-Host ""

# Lancer le backend
cd backend
python main.py
