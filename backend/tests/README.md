# Tests - Backend Immobilier API

## Structure des tests

```
tests/
├── __init__.py
├── test_passwords.py          # Tests unitaires des mots de passe
└── test_auth_endpoints.py      # Tests des endpoints d'authentification
```

## Classes de tests

### test_passwords.py

#### TestPasswordValidation
- ✅ `test_password_valid_simple` - Mot de passe simple
- ✅ `test_password_valid_special_chars` - Caractères spéciaux
- ✅ `test_password_valid_unicode` - Caractères unicode
- ✅ `test_password_valid_long_but_under_72_bytes` - Long mais valide
- ✅ `test_password_valid_immobilier_example` - Exemple du projet
- ✅ `test_password_invalid_over_72_bytes` - Rejeté > 72 bytes
- ✅ `test_password_invalid_unicode_over_72_bytes` - Unicode rejeté > 72 bytes

#### TestPasswordTruncation
- ✅ `test_truncate_password_under_limit` - Sous la limite
- ✅ `test_truncate_password_at_limit` - À la limite
- ✅ `test_truncate_password_over_limit` - Au-dessus de la limite
- ✅ `test_truncate_unicode_password` - Unicode tronqué proprement

#### TestPasswordHashing
- ✅ `test_hash_password_basic` - Hashage basique
- ✅ `test_hash_password_different_results` - Hashes différents (salt)
- ✅ `test_verify_password_correct` - Vérification correcte
- ✅ `test_verify_password_incorrect` - Vérification échouée
- ✅ `test_hash_and_verify_long_password` - Long mot de passe
- ✅ `test_hash_and_verify_unicode_password` - Unicode
- ✅ `test_hash_and_verify_special_chars` - Caractères spéciaux

#### TestPasswordExamples
- ✅ `test_immobilier_password` - Mot de passe "immobilier@01"
- ✅ `test_complex_passwords` - Mots de passe complexes variés

#### TestEdgeCases
- ✅ `test_empty_password` - Mot de passe vide
- ✅ `test_whitespace_password` - Espaces blancs
- ✅ `test_password_with_newlines` - Sauts de ligne
- ✅ `test_password_case_sensitive` - Sensibilité à la casse

### test_auth_endpoints.py

#### TestRegistrationEndpoint
- ✅ `test_register_valid_user` - Enregistrement valide
- ✅ `test_register_password_too_long` - Mot de passe trop long
- ✅ `test_register_duplicate_username` - Username dupliqué
- ✅ `test_register_duplicate_email` - Email dupliqué
- ✅ `test_register_immobilier_password` - Avec password "immobilier@01"

#### TestLoginEndpoint
- ✅ `test_login_valid_credentials` - Identifiants valides
- ✅ `test_login_invalid_username` - Username invalide
- ✅ `test_login_invalid_password` - Mot de passe invalide
- ✅ `test_login_case_sensitive_username` - Sensibilité à la casse

#### TestMeEndpoint
- ✅ `test_get_current_user_authenticated` - Utilisateur avec token
- ✅ `test_get_current_user_no_token` - Sans token
- ✅ `test_get_current_user_invalid_token` - Token invalide

## Lancer les tests

### Tous les tests
```bash
python run_tests.py
```

Ou directement avec pytest :
```bash
pytest tests/ -v
```

### Tests spécifiques
```bash
# Seulement les tests de password
pytest tests/test_passwords.py -v

# Seulement les tests d'endpoints
pytest tests/test_auth_endpoints.py -v

# Un test spécifique
pytest tests/test_passwords.py::TestPasswordValidation::test_password_valid_immobilier_example -v
```

### Avec coverage (couverture de code)
```bash
pytest tests/ --cov=app --cov-report=html
```

## Mots de passe testés

### Autorisés ✅
- `simplePassword123` - 18 caractères
- `P@ssw0rd!#$%&*()` - 16 caractères avec spéciaux
- `Pässwörd123ñ` - 12 caractères unicode
- `immobilier@01` - 13 caractères (exemple du projet)
- Tout mot de passe < 72 bytes UTF-8

### Rejetés ❌
- Mots de passe > 72 bytes UTF-8
- Exemple : `"x" * 100` (100 bytes)

## Notes importantes

1. **Limite bcrypt** : bcrypt (via passlib) a une limite de 72 bytes (pas caractères)
2. **UTF-8** : Les caractères unicode peuvent prendre 1-4 bytes
3. **Case-sensitive** : Les mots de passe respectent la casse
4. **Salt** : Chaque hash génère un salt différent
5. **Historique** : Chaque changement est enregistré dans `password_history`

## Exemple de test unitaire

```python
def test_immobilier_password(self):
    """Test the immobilier@01 password"""
    password = "immobilier@01"
    
    # Hash
    hashed = auth_service.hash_password(password)
    
    # Verify
    is_valid = auth_service.verify_password(password, hashed)
    
    assert is_valid is True
```
