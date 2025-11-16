#!/usr/bin/env python3
"""
Test qui provoque une VRAIE exception pour voir le stack trace complet
"""

import pytest
import logging
from fastapi.testclient import TestClient
from conftest import client

logger = logging.getLogger("auth")


class TestRealExceptions:
    """Tests qui provoquent des vraies exceptions"""
    
    def test_cause_attribute_error(self):
        """
        Test qui provoque une AttributeError (vraie exception)
        """
        print("\n" + "="*80)
        print("TEST: Force une AttributeError")
        print("="*80)
        
        logger.info("🔴 Début du test - provoquant une exception")
        
        try:
            # Créer une exception intentionnelle
            obj = None
            value = obj.some_attribute  # AttributeError: 'NoneType' object has no attribute
        except AttributeError as e:
            # Cela va logger le stack trace
            logger.error(f"AttributeError capturée: {str(e)}", exc_info=True)
        
        print("\n✅ Exception loggée - vérifiez les logs pour le stack trace")
        print("="*80 + "\n")
    
    def test_cause_type_error(self):
        """
        Test qui provoque une TypeError
        """
        print("\n" + "="*80)
        print("TEST: Force une TypeError")
        print("="*80)
        
        logger.info("🔴 Début du test - provoquant une TypeError")
        
        try:
            # Créer une TypeError
            result = "string" + 123  # TypeError: can only concatenate str with str
        except TypeError as e:
            # Cela va logger le stack trace
            logger.error(f"TypeError capturée: {str(e)}", exc_info=True)
        
        print("\n✅ Exception loggée - vérifiez les logs pour le stack trace")
        print("="*80 + "\n")
    
    def test_cause_division_error(self):
        """
        Test qui provoque une ZeroDivisionError
        """
        print("\n" + "="*80)
        print("TEST: Force une ZeroDivisionError")
        print("="*80)
        
        logger.info("🔴 Début du test - provoquant une ZeroDivisionError")
        
        try:
            # Division par zéro
            result = 10 / 0
        except ZeroDivisionError as e:
            # Cela va logger le stack trace
            logger.error(f"ZeroDivisionError capturée: {str(e)}", exc_info=True)
        
        print("\n✅ Exception loggée - vérifiez les logs pour le stack trace")
        print("="*80 + "\n")
    
    def test_nested_exception(self):
        """
        Test avec exception imbriquée pour voir le stack trace complet
        """
        print("\n" + "="*80)
        print("TEST: Exception imbriquée (stack trace complet)")
        print("="*80)
        
        logger.info("🔴 Début du test - provoquant une exception imbriquée")
        
        def level_3():
            logger.debug("  [Level 3] Appel à une fonction inexistante")
            return undefined_function()  # NameError
        
        def level_2():
            logger.debug(" [Level 2] Appelant level_3")
            return level_3()
        
        def level_1():
            logger.debug("[Level 1] Appelant level_2")
            return level_2()
        
        try:
            logger.info("Appelant level_1")
            level_1()
        except NameError as e:
            # Cela va logger le stack trace COMPLET avec tous les niveaux
            logger.error(f"NameError capturée: {str(e)}", exc_info=True)
        
        print("\n✅ Exception imbriquée loggée - vérifiez les logs pour le stack trace complet")
        print("="*80 + "\n")


if __name__ == "__main__":
    """
    Pour exécuter ces tests:
    cd backend
    python -m pytest tests/test_real_exceptions.py -v -s
    """
    pytest.main([__file__, "-v", "-s"])
