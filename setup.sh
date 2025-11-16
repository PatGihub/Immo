#!/bin/bash

# Script de démarrage du projet Immobilier
# Démarre à la fois le frontend et le backend

echo "🚀 Démarrage du projet Immobilier..."
echo ""

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier si les répertoires existent
if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    echo "❌ Erreur: Les répertoires frontend et backend ne sont pas trouvés"
    exit 1
fi

echo -e "${BLUE}📦 Installation des dépendances...${NC}"
echo ""

# Frontend
echo -e "${GREEN}Frontend:${NC}"
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
echo "✅ Frontend prêt"
cd ..

echo ""

# Backend
echo -e "${GREEN}Backend:${NC}"
cd backend
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activer venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    # Windows
    source venv/Scripts/activate 2>/dev/null || true
fi

if ! pip list | grep -q "fastapi"; then
    pip install -r requirements.txt
fi
echo "✅ Backend prêt"
cd ..

echo ""
echo -e "${BLUE}🎯 Prochaines étapes:${NC}"
echo ""
echo "1. Démarrer le backend (dans un terminal):"
echo -e "   ${GREEN}cd backend${NC}"
echo -e "   ${GREEN}source venv/bin/activate${NC}  # ou venv\\Scripts\\activate sur Windows"
echo -e "   ${GREEN}python main.py${NC}"
echo ""
echo "2. Démarrer le frontend (dans un autre terminal):"
echo -e "   ${GREEN}cd frontend${NC}"
echo -e "   ${GREEN}npm run dev${NC}"
echo ""
echo "3. Ouvrir votre navigateur:"
echo -e "   ${GREEN}Frontend: http://localhost:5173${NC}"
echo -e "   ${GREEN}API Docs: http://localhost:8000/docs${NC}"
echo ""
