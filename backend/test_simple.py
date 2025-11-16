#!/usr/bin/env python3
"""Simple test to debug password hashing"""

from app.services.auth import auth_service

def test_simple():
    """Test simple password hashing - like the working example"""
    print("\n" + "="*60)
    print("TEST AVEC VOTRE EXEMPLE : azertjilo123")
    print("="*60)
    
    # Exactement comme votre exemple
    mot_de_passe = "azertjilo123"
    
    print(f"\n1. Mot de passe: '{mot_de_passe}'")
    
    try:
        # Hachage
        hash_mdp = auth_service.hash_password(mot_de_passe)
        print(f"\n2. Hash enregistré: {hash_mdp}")
        
        # Test avec le bon mot de passe
        mot_a_tester = "azertjilo123"
        if auth_service.verify_password(mot_a_tester, hash_mdp):
            print(f"\n3. ✅ Mot de passe valide!")
        else:
            print(f"\n3. ❌ Mot de passe invalide")
        
        # Test avec mauvais mot de passe
        mot_faux = "azertjilo456"
        if auth_service.verify_password(mot_faux, hash_mdp):
            print(f"\n4. ❌ Mauvais mot de passe accepté (erreur!)")
        else:
            print(f"\n4. ✅ Mauvais mot de passe rejeté")
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()

