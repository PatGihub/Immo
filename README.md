# Immobilier - Full Stack Application

Une application full-stack pour la gestion de propriétés immobilières avec une interface React/TypeScript moderne et une API Python FastAPI robuste.

## 📋 Structure du Projet

```
Immobilier/
├── frontend/                 # Interface React/TypeScript
│   ├── src/
│   │   ├── components/      # Composants React réutilisables
│   │   ├── pages/           # Pages principales
│   │   ├── hooks/           # Hooks React personnalisés
│   │   ├── utils/           # Utilitaires et helpers
│   │   ├── styles/          # Feuilles de style
│   │   ├── main.tsx         # Point d'entrée
│   │   └── App.tsx          # Composant principal
│   ├── package.json         # Dépendances npm
│   ├── tsconfig.json        # Configuration TypeScript
│   ├── vite.config.ts       # Configuration Vite
│   └── .env.*               # Variables d'environnement
│
├── backend/                  # API Python FastAPI
│   ├── app/
│   │   ├── routes/          # Routes API
│   │   ├── models/          # Modèles de données (SQLAlchemy)
│   │   ├── schemas/         # Schémas Pydantic
│   │   ├── middleware/      # Middleware personnalisé
│   │   ├── database/        # Configuration base de données
│   │   └── config.py        # Configuration application
│   ├── main.py              # Point d'entrée FastAPI
│   ├── requirements.txt      # Dépendances Python
│   └── .env*                # Variables d'environnement
│
└── README.md                # Ce fichier
```

## 🚀 Démarrage Rapide

### Prérequis

- Node.js 18+ et npm
- Python 3.9+

### Installation et Lancement

#### 1. Frontend (React/TypeScript/Vite)

```bash
cd frontend
npm install
npm run dev
```

L'interface sera accessible sur `http://localhost:5173`

#### 2. Backend (FastAPI)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

L'API sera accessible sur `http://localhost:8000`
- Documentation Swagger: `http://localhost:8000/docs`
- Documentation ReDoc: `http://localhost:8000/redoc`

## 📁 Guide des Dossiers

### Frontend (`/frontend`)

**Configuration:**
- `package.json` - Gestion des dépendances npm
- `tsconfig.json` - Configuration TypeScript
- `vite.config.ts` - Configuration du bundler Vite
- `.env.development` - Variables d'environnement développement
- `.env.production` - Variables d'environnement production

**Source (`src/`):**
- `components/` - Composants React réutilisables
- `pages/` - Pages principales de l'application
- `hooks/` - Hooks personnalisés (useFetch, etc.)
- `utils/` - Fonctions utilitaires (API client, formatters, etc.)
- `styles/` - Feuilles de style CSS

### Backend (`/backend`)

**Application (`app/`):**
- `routes/` - Points de terminaison API
  - `health.py` - Vérification d'état
  - `__init__.py` - Routes pour les propriétés
- `models/` - Modèles SQLAlchemy (User, Property)
- `schemas/` - Schémas Pydantic pour validation
- `database/` - Configuration SQLAlchemy et sessions DB
- `middleware/` - Middleware personnalisés (CORS, Auth, etc.)
- `config.py` - Configuration centralisée

**Fichiers Root:**
- `main.py` - Application FastAPI
- `requirements.txt` - Dépendances Python
- `.env` - Configuration locale

## 🔧 Configuration

### Variables d'Environnement Frontend

```env
VITE_API_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000
```

### Variables d'Environnement Backend

```env
DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./immobilier.db
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 📦 Dépendances

### Frontend
- **React 18** - Bibliothèque UI
- **TypeScript** - Typage statique
- **Vite** - Bundler rapide
- **React Router** - Navigation
- **Axios** - Client HTTP

### Backend
- **FastAPI** - Framework web moderne
- **Uvicorn** - Serveur ASGI
- **SQLAlchemy** - ORM base de données
- **Pydantic** - Validation de données
- **python-dotenv** - Gestion des variables d'environnement

## 🛣️ Routes API Principales

### Health Check
- `GET /health` - Vérification de l'état de l'API

### Propriétés
- `GET /api/properties` - Lister toutes les propriétés
- `GET /api/properties/{id}` - Obtenir une propriété
- `POST /api/properties` - Créer une propriété
- `PUT /api/properties/{id}` - Mettre à jour une propriété
- `DELETE /api/properties/{id}` - Supprimer une propriété

## 🔐 Sécurité

- CORS configuré pour les domaines locaux
- Validation Pydantic pour toutes les entrées
- TypeScript strict pour le typage
- Variables sensibles dans `.env` (non commité)

## 🐛 Développement

### Scripts Frontend
- `npm run dev` - Mode développement avec rechargement automatique
- `npm run build` - Build production
- `npm run preview` - Aperçu du build
- `npm run lint` - Vérification du code
- `npm run type-check` - Vérification TypeScript

### Scripts Backend
```bash
# Développement avec rechargement automatique
python main.py

# Ou avec uvicorn directement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Prochaines Étapes

1. **Authentification** - Implémenter JWT et gestion d'utilisateurs
2. **Base de données** - Passer de SQLite à PostgreSQL en production
3. **Tests** - Ajouter des tests unitaires et d'intégration
4. **Déploiement** - Configurer CI/CD et déploiement
5. **Documentation** - Améliorer les docstrings et la documentation

## 📄 License

MIT

## 👨‍💻 Support

Pour toute question ou problème, créez une issue ou consultez la documentation.
