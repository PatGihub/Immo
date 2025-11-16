#!/usr/bin/env python3
"""
Test d'authentification qui ÉCHOUE intentionnellement
Utile pour voir les logs d'exception en détail
"""

import pytest
from fastapi.testclient import TestClient
from conftest import client


class TestAuthenticationFailures:
    """Tests d'authentification qui échouent - pour voir les logs d'erreur"""
    
    def test_login_with_wrong_password(self, client: TestClient):
        """
        Test qui échoue : Login avec mauvais mot de passe
        Permet de voir les logs d'erreur en détail
        """
        print("\n" + "="*80)
        print("TEST D'AUTHENTIFICATION ÉCHOUÉE - Mauvais mot de passe")
        print("="*80)
        
        # D'abord créer un utilisateur
        register_response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser_fail",
                "email": "test_fail@example.com",
                "password": "CorrectPassword123"
            }
        )
        assert register_response.status_code == 201
        print("\n✅ Utilisateur créé avec password: CorrectPassword123")
        
        # Essayer de se connecter avec un MAUVAIS mot de passe
        print("\n❌ Tentative de login avec mot de passe INCORRECT: WrongPassword456")
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser_fail",
                "password": "WrongPassword456"  # MAUVAIS !
            }
        )
        
        # Vérifier que ça échoue
        print(f"\nStatus Code: {login_response.status_code}")
        print(f"Response: {login_response.json()}")
        
        assert login_response.status_code == 401, "Login devrait échouer avec mauvais password"
        print("\n✅ Erreur 401 attendue - Vérifiez les logs pour voir les détails")
        print("="*80 + "\n")
    
    def test_login_nonexistent_user(self, client: TestClient):
        """
        Test qui échoue : Login utilisateur inexistant
        """
        print("\n" + "="*80)
        print("TEST D'AUTHENTIFICATION ÉCHOUÉE - Utilisateur inexistant")
        print("="*80)
        
        print("\n❌ Tentative de login avec utilisateur inexistant: ghost_user")
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "ghost_user",
                "password": "any_password"
            }
        )
        
        print(f"\nStatus Code: {login_response.status_code}")
        print(f"Response: {login_response.json()}")
        
        assert login_response.status_code == 401
        print("\n✅ Erreur 401 attendue - Vérifiez les logs")
        print("="*80 + "\n")
    
    def test_get_user_without_token(self, client: TestClient):
        """
        Test qui échoue : Accéder à /me sans token
        """
        print("\n" + "="*80)
        print("TEST ÉCHOUÉE - Pas de token d'authentification")
        print("="*80)
        
        print("\n❌ Tentative d'accès à /me sans Authorization header")
        response = client.get("/api/auth/me")
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 401
        print("\n✅ Erreur 401 attendue - Vérifiez les logs")
        print("="*80 + "\n")
    
    def test_get_user_with_invalid_token(self, client: TestClient):
        """
        Test qui échoue : Token invalide
        """
        print("\n" + "="*80)
        print("TEST ÉCHOUÉE - Token invalide")
        print("="*80)
        
        print("\n❌ Tentative d'accès avec token INVALIDE")
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token_xyz"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 401
        print("\n✅ Erreur 401 attendue - Vérifiez les logs")
        print("="*80 + "\n")
    
    def test_register_duplicate_username(self, client: TestClient):
        """
        Test qui échoue : Enregistrer avec username déjà existant
        """
        print("\n" + "="*80)
        print("TEST ÉCHOUÉE - Username en doublon")
        print("="*80)
        
        # Créer un premier utilisateur
        client.post(
            "/api/auth/register",
            json={
                "username": "duplicate_user",
                "email": "duplicate1@example.com",
                "password": "Password123"
            }
        )
        print("✅ Premier utilisateur créé: duplicate_user")
        
        # Essayer de créer un second avec le même username
        print("\n❌ Tentative de créer un deuxième utilisateur avec le même username")
        response = client.post(
            "/api/auth/register",
            json={
                "username": "duplicate_user",  # MÊME USERNAME !
                "email": "duplicate2@example.com",
                "password": "Password456"
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        assert response.status_code == 400
        print("\n✅ Erreur 400 attendue - Vérifiez les logs")
        print("="*80 + "\n")
    
    def test_password_too_long(self, client: TestClient):
        """
        Test qui échoue : Mot de passe trop long (>72 bytes en UTF-8)
        """
        print("\n" + "="*80)
        print("TEST ÉCHOUÉE - Mot de passe trop long (>72 bytes)")
        print("="*80)
        
        # Créer un mot de passe de plus de 72 bytes
        long_password = "A" * 100  # 100 caractères = 100 bytes en ASCII
        
        print(f"\n❌ Tentative avec mot de passe de {len(long_password)} caractères")
        response = client.post(
            "/api/auth/register",
            json={
                "username": "longpass_user",
                "email": "longpass@example.com",
                "password": long_password
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Ce test peut échouer ou réussir selon la validation
        # (la troncation automatique peut s'appliquer)
        print("\n📊 Vérifiez les logs pour voir comment le mot de passe long est traité")
        print("="*80 + "\n")


if __name__ == "__main__":
    """
    Pour exécuter ces tests:
    cd backend
    python -m pytest tests/test_auth_failures.py -v -s
    
    Les tests vont volontairement échouer pour montrer les logs d'erreur
    """
    pytest.main([__file__, "-v", "-s"])
