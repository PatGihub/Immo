# Immobilier Backend API

API FastAPI pour la gestion des propriétés immobilières.

## 🛠️ Stack Technologique

- **FastAPI** - Framework web moderne
- **Python 3.9+** - Langage de programmation
- **SQLAlchemy** - ORM pour la base de données
- **Pydantic** - Validation de données
- **Uvicorn** - Serveur ASGI
- **CORS** - Cross-Origin Resource Sharing

## 📦 Installation

### Avec virtualenv

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## 🚀 Démarrage

```bash
python main.py
```

L'API sera disponible sur: `http://localhost:8000`

### Documentation Interactive

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Structure

```
app/
├── routes/           # Points de terminaison API
│   ├── health.py    # Vérification d'état
│   └── __init__.py  # Routes pour propriétés
├── models/           # Modèles SQLAlchemy
├── schemas/          # Schémas Pydantic
├── database/         # Configuration BD
├── middleware/       # Middlewares personnalisés
└── config.py         # Configuration app

main.py              # Point d'entrée FastAPI
requirements.txt     # Dépendances
.env                 # Variables d'environnement
```

## 🔌 Endpoints Principaux

### Health
```
GET /health
GET /
```

### Propriétés
```
GET /properties                 # Liste toutes les propriétés
GET /properties/{id}            # Obtenir une propriété
POST /properties                # Créer une propriété
PUT /properties/{id}            # Mettre à jour
DELETE /properties/{id}         # Supprimer
```

## 📊 Modèles de Données

### User
- id: int
- username: str (unique)
- email: str (unique)
- hashed_password: str
- is_active: bool
- created_at: datetime
- updated_at: datetime

### Property
- id: int
- title: str
- description: str
- price: int
- location: str
- rooms: int (optionnel)
- bathrooms: int (optionnel)
- area: int (optionnel, en m²)
- created_at: datetime
- updated_at: datetime

## 🔐 Configuration

Variables d'environnement (.env):

```env
DEBUG=True
SECRET_KEY=votre-clé-secrète
DATABASE_URL=sqlite:///./immobilier.db
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🧪 Test de l'API

### Avec cURL

```bash
# GET /health
curl http://localhost:8000/health

# GET /properties
curl http://localhost:8000/api/properties

# POST /properties
curl -X POST http://localhost:8000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bel appartement",
    "price": 250000,
    "location": "Paris",
    "rooms": 3
  }'
```

### Avec Python Requests

```python
import requests

# GET
response = requests.get('http://localhost:8000/api/properties')
print(response.json())

# POST
data = {
    "title": "Maison luxe",
    "price": 500000,
    "location": "Toulouse",
    "rooms": 4
}
response = requests.post('http://localhost:8000/api/properties', json=data)
print(response.json())
```

## 🛠️ Développement

### Avec rechargement automatique
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Avec environment de production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Uvicorn Docs](https://www.uvicorn.org/)

## 🔜 Prochaines Étapes

- [ ] Authentification JWT
- [ ] Tests unitaires
- [ ] Logging avancé
- [ ] Cache Redis
- [ ] Migration vers PostgreSQL
- [ ] Docker support
