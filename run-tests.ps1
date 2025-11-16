# Script pour lancer les tests unitaires du backend

Write-Host "Lancement des tests unitaires..." -ForegroundColor Green
Write-Host ""

# Aller à la racine du projet
cd c:\02_Data\01_Learning\Project\Immobilier

# Activer le venv
Write-Host "Activation du venv..." -ForegroundColor Blue
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Lancement des tests..." -ForegroundColor Cyan
Write-Host ""

# Aller dans le backend
cd backend

# Lancer les tests
python -m pytest tests/test_passwords.py -v

Write-Host ""
Write-Host "Tests termines!" -ForegroundColor Green
