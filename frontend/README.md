# Immobilier Frontend

Interface utilisateur moderne pour l'application de gestion immobilière.

## 🛠️ Stack Technologique

- **React 18** - Bibliothèque de composants
- **TypeScript** - Langage typé
- **Vite** - Bundler moderne et ultra-rapide
- **React Router** - Gestion de la navigation
- **Axios** - Client HTTP
- **ESLint** - Linting du code

## 📦 Installation

```bash
npm install
```

## 🚀 Développement

```bash
npm run dev
```

Accessible sur: `http://localhost:5173`

## 🏗️ Build Production

```bash
npm run build
npm run preview
```

## 📝 Commandes Disponibles

- `npm run dev` - Démarrer le serveur de développement
- `npm run build` - Créer un build production
- `npm run preview` - Prévisualiser le build
- `npm run lint` - Vérifier le code
- `npm run type-check` - Vérifier les types TypeScript

## 📁 Structure

```
src/
├── components/   # Composants réutilisables
├── pages/        # Pages de l'application
├── hooks/        # Hooks personnalisés
├── utils/        # Fonctions utilitaires
├── styles/       # Styles CSS
├── main.tsx      # Point d'entrée
└── App.tsx       # Composant racine
```

## 🔌 API Integration

L'application se connecte à l'API backend sur:
- Développement: `http://localhost:8000/api`
- Production: Variable VITE_API_URL dans .env

Utilisez le hook `useFetch` pour les requêtes:

```typescript
const { data, loading, error } = useFetch<PropertyResponse>('/properties')
```

## 🎨 Styles

Les styles CSS sont organisés dans `src/styles/`:
- `index.css` - Styles globaux
- `App.css` - Styles du composant principal

## 📚 Ressources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router Docs](https://reactrouter.com)
