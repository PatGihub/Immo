#!/usr/bin/env python3
"""
Test pour démontrer le logging détaillé avec stack trace formaté
"""

import pytest
import logging
from fastapi.testclient import TestClient
from conftest import client
from app.utils.logging_utils import log_exception_with_traceback, log_full_traceback

logger = logging.getLogger("auth")


class TestLoggingStackTrace:
    """Tests pour démontrer le logging formaté"""
    
    def test_log_exception_with_context(self, client: TestClient):
        """
        Teste le logging d'exception avec contexte
        """
        print("\n" + "="*80)
        print("TEST: Logging exception avec contexte formaté")
        print("="*80)
        
        try:
            # Créer une erreur intentionnellement
            result = 1 / 0  # Division par zéro
        except Exception as e:
            # Logger avec contexte
            log_exception_with_traceback(
                logger,
                e,
                context={
                    "operation": "division",
                    "numerator": 1,
                    "denominator": 0,
                    "timestamp": "2025-11-16 13:40:00"
                }
            )
        
        print("\n✅ Exception loggée avec stack trace formaté")
        print("📊 Vérifiez les logs pour voir le formatage")
        print("="*80 + "\n")
    
    def test_log_full_traceback(self):
        """
        Teste le logging du stack trace complet
        """
        print("\n" + "="*80)
        print("TEST: Logging stack trace complet")
        print("="*80)
        
        # Logger le stack trace complet du point courant
        log_full_traceback(logger, "Full Application Stack")
        
        print("\n✅ Stack trace complet loggé")
        print("📊 Vérifiez les logs pour voir le stack trace")
        print("="*80 + "\n")
    
    def test_register_and_log_process(self, client: TestClient):
        """
        Test d'enregistrement avec logging détaillé du processus
        """
        print("\n" + "="*80)
        print("TEST: Enregistrement avec logging du processus")
        print("="*80)
        
        logger.info("=" * 60)
        logger.info("DÉBUT: Enregistrement nouvel utilisateur")
        logger.info("=" * 60)
        
        try:
            logger.info("Étape 1: Validation des données")
            user_data = {
                "username": "traceback_user",
                "email": "traceback@example.com",
                "password": "TracedPassword123"
            }
            logger.debug(f"Données validées: {user_data}")
            
            logger.info("Étape 2: Appel POST /api/auth/register")
            response = client.post("/api/auth/register", json=user_data)
            logger.debug(f"Réponse reçue: status={response.status_code}")
            
            logger.info("Étape 3: Vérification du résultat")
            if response.status_code == 201:
                logger.info("✅ Enregistrement réussi!")
                logger.debug(f"Réponse: {response.json()}")
            else:
                logger.error(f"❌ Erreur lors de l'enregistrement: {response.json()}")
            
            logger.info("=" * 60)
            logger.info("FIN: Enregistrement")
            logger.info("=" * 60)
            
        except Exception as e:
            log_exception_with_traceback(
                logger,
                e,
                context={
                    "operation": "register_user",
                    "username": user_data.get("username")
                }
            )
        
        print("\n✅ Processus d'enregistrement loggé en détail")
        print("📊 Vérifiez les logs pour voir tous les détails")
        print("="*80 + "\n")


if __name__ == "__main__":
    """
    Pour exécuter ces tests:
    cd backend
    python -m pytest tests/test_logging_stacktrace.py -v -s
    """
    pytest.main([__file__, "-v", "-s"])
