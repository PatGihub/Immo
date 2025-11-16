#!/usr/bin/env python3
"""
Test qui force une VRAIE exception pour voir le stack trace complet
"""

import pytest
from fastapi.testclient import TestClient
from conftest import client


class TestExceptionStackTrace:
    """Tests qui génèrent des vraies exceptions"""
    
    def test_force_database_error(self, client: TestClient):
        """
        Force une erreur base de données pour voir le stack trace
        """
        print("\n" + "="*80)
        print("TEST: Force une exception base de données")
        print("="*80)
        
        # Envoyer une requête avec email INVALIDE (non-string)
        # Cela devrait causer une erreur de validation Pydantic
        print("\n❌ Envoi de données invalides (email = nombre)")
        response = client.post(
            "/api/auth/register",
            json={
                "username": "test_user",
                "email": 12345,  # EMAIL INVALIDE - nombre au lieu de string
                "password": "Password123"
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("\n📊 Vérifiez les logs pour voir l'exception complète")
        print("="*80 + "\n")
    
    def test_force_password_hash_error(self, client: TestClient):
        """
        Force une erreur lors du hachage du mot de passe
        """
        print("\n" + "="*80)
        print("TEST: Force une exception hachage mot de passe")
        print("="*80)
        
        # Envoyer un mot de passe qui est un objet (pas une string)
        # Cela devrait causer une exception dans hash_password
        print("\n❌ Mot de passe invalide (objet au lieu de string)")
        response = client.post(
            "/api/auth/register",
            json={
                "username": "test_user",
                "email": "test@example.com",
                "password": None  # PASSWORD INVALIDE - None au lieu de string
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("\n📊 Vérifiez les logs pour voir l'exception complète")
        print("="*80 + "\n")
    
    def test_register_with_invalid_json(self, client: TestClient):
        """
        Envoie du JSON invalide
        """
        print("\n" + "="*80)
        print("TEST: JSON invalide")
        print("="*80)
        
        print("\n❌ JSON invalide (pas de password)")
        response = client.post(
            "/api/auth/register",
            json={
                "username": "test_user",
                "email": "test@example.com"
                # PASSWORD MANQUANT
            }
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("\n📊 Vérifiez les logs pour voir l'exception complète")
        print("="*80 + "\n")


if __name__ == "__main__":
    """
    Pour exécuter ces tests:
    cd backend
    python -m pytest tests/test_exception_stacktrace.py -v -s
    """
    pytest.main([__file__, "-v", "-s"])
