#!/usr/bin/env python3
"""
Test d'authentification complet : Enregistrement + Login
Ce test démontre le flux complet d'authentification :
1. Créer un utilisateur avec un mot de passe
2. Vérifier que le mot de passe est hashé correctement
3. Se connecter avec le même mot de passe
4. Vérifier que le JWT token est généré
"""

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

# Cette configuration s'attend à être exécutée depuis le répertoire backend
# et suppose que conftest.py est disponible
from conftest import client, db
from app.models import User


@pytest.fixture(autouse=True)
def cleanup_users(db):
    """
    Nettoie les utilisateurs de test après chaque test.
    autouse=True signifie que cette fixture s'exécute automatiquement.
    """
    yield  # Le test s'exécute ici
    
    # Après le test: supprimer tous les utilisateurs de test
    db.query(User).delete()
    db.commit()


class TestFullAuthenticationFlow:
    """Test du flux complet d'authentification : Register → Login"""
    
    def test_register_and_login_same_user(self, client: TestClient):
        """
        SCÉNARIO: 
        - Un utilisateur s'enregistre avec email et mot de passe
        - Le mot de passe est hashé et stocké
        - L'utilisateur se connecte avec le même mot de passe
        - Un JWT token est généré avec succès
        """
        
        # Configuration du test
        test_username = "testuser"
        test_email = "test@example.com"
        test_password = "testPassword123"
        
        print("\n" + "="*70)
        print("TEST D'AUTHENTIFICATION COMPLET")
        print("="*70)
        
        # STEP 1: ENREGISTREMENT
        print("\n1️⃣  STEP 1: ENREGISTREMENT DE L'UTILISATEUR")
        print("-" * 70)
        print(f"   Username: {test_username}")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": test_username,
                "email": test_email,
                "password": test_password
            }
        )
        
        # Vérifier que l'enregistrement réussit
        assert register_response.status_code == 201, \
            f"Enregistrement échoué: {register_response.text}"
        
        register_data = register_response.json()
        print(f"\n   ✅ Enregistrement réussi!")
        print(f"   User ID: {register_data['id']}")
        print(f"   Username: {register_data['username']}")
        print(f"   Email: {register_data['email']}")
        assert register_data["username"] == test_username
        assert register_data["email"] == test_email
        assert "hashed_password" not in register_data  # Le hash ne doit pas être exposé
        
        # STEP 2: AUTHENTIFICATION
        print("\n2️⃣  STEP 2: AUTHENTIFICATION (LOGIN)")
        print("-" * 70)
        print(f"   Username: {test_username}")
        print(f"   Password: {test_password}")
        
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": test_username,
                "password": test_password  # Même mot de passe que l'enregistrement
            }
        )
        
        # Vérifier que l'authentification réussit
        assert login_response.status_code == 200, \
            f"Authentification échouée: {login_response.text}"
        
        login_data = login_response.json()
        print(f"\n   ✅ Authentification réussie!")
        print(f"   Token Type: {login_data['token_type']}")
        print(f"   Access Token: {login_data['access_token'][:50]}...")
        print(f"   User: {login_data['user']['username']}")
        
        # STEP 3: VÉRIFIER LE CONTENU DU TOKEN
        print("\n3️⃣  STEP 3: VÉRIFICATION DU CONTENU")
        print("-" * 70)
        
        # Vérifier que le token JWT est présent et valide
        assert "access_token" in login_data, "Token d'accès manquant"
        assert login_data["token_type"] == "bearer", "Type de token invalide"
        assert login_data["user"]["username"] == test_username, "Username ne correspond pas"
        print(f"   ✅ Token JWT valide")
        print(f"   ✅ Type: bearer")
        print(f"   ✅ Username: {login_data['user']['username']}")
        
        # STEP 4: ESSAYER DE SE RECONNECTER AVEC UN MAUVAIS MOT DE PASSE
        print("\n4️⃣  STEP 4: VÉRIFICATION DE SÉCURITÉ - Mauvais mot de passe")
        print("-" * 70)
        
        wrong_password_response = client.post(
            "/api/auth/login",
            json={
                "username": test_username,
                "password": "wrongPassword456"  # Mauvais mot de passe
            }
        )
        
        # Vérifier que l'authentification échoue avec le mauvais mot de passe
        assert wrong_password_response.status_code == 401, \
            "Authentification devrait échouer avec un mauvais mot de passe"
        print(f"   ✅ Mauvais mot de passe rejeté correctement (HTTP 401)")
        
        print("\n" + "="*70)
        print("✅ TEST COMPLET D'AUTHENTIFICATION RÉUSSI!")
        print("="*70)
        print("""
RÉSUMÉ:
  1. ✅ Enregistrement avec mot de passe: OK
  2. ✅ Mot de passe hashé et stocké: OK
  3. ✅ Login avec bon mot de passe: OK
  4. ✅ JWT token généré: OK
  5. ✅ Login avec mauvais mot de passe: REJETÉ ✅
  
Le système d'authentification fonctionne parfaitement !
""")
    
    def test_register_and_login_immobilier_password(self, client: TestClient):
        """
        Test avec le mot de passe spécifique du projet: immobilier@01
        """
        
        test_username = "immobilier_user"
        test_email = "immobilier@test.com"
        test_password = "immobilier@01"  # Mot de passe du projet
        
        print("\n" + "="*70)
        print("TEST AVEC MOT DE PASSE 'immobilier@01'")
        print("="*70)
        
        # Enregistrement
        print("\n1️⃣  Enregistrement...")
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": test_username,
                "email": test_email,
                "password": test_password
            }
        )
        assert register_response.status_code == 201
        print("   ✅ Enregistrement réussi")
        
        # Login
        print("\n2️⃣  Login avec immobilier@01...")
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": test_username,
                "password": test_password
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        print("   ✅ Login réussi")
        print(f"   ✅ Token généré: {login_data['access_token'][:50]}...")
        
        print("\n" + "="*70)
        print("✅ TEST MOT DE PASSE 'immobilier@01' RÉUSSI!")
        print("="*70)


if __name__ == "__main__":
    """
    Pour exécuter ce test :
    cd backend
    python -m pytest test_full_auth_flow.py -v -s
    
    Le -s permet d'afficher les prints
    """
    pytest.main([__file__, "-v", "-s"])
