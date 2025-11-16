#!/usr/bin/env python3
"""Test authentication for existing user"""

from sqlalchemy import create_engine, text
from app.services.auth import auth_service
import bcrypt

print("\n" + "="*70)
print("TEST D'AUTHENTIFICATION - UTILISATEUR EXISTANT")
print("="*70)

# 1. Get existing user from database
engine = create_engine('sqlite:///./immobilier.db')
conn = engine.connect()

print("\n1️⃣  RECHERCHE DE L'UTILISATEUR PATRICK")
print("-" * 70)

result = conn.execute(text('SELECT id, username, email, hashed_password FROM users WHERE username = "Patrick"'))
user_row = result.fetchone()

if not user_row:
    print("❌ Utilisateur Patrick non trouvé!")
    conn.close()
    exit(1)

user_id, username, email, stored_hash = user_row
print(f"✅ Utilisateur trouvé:")
print(f"   ID: {user_id}")
print(f"   Username: {username}")
print(f"   Email: {email}")
print(f"   Stored hash: {stored_hash[:50]}...")

# 2. Get password history
print("\n2️⃣  HISTORIQUE DES MOTS DE PASSE")
print("-" * 70)

result = conn.execute(text('SELECT id, reason, changed_at FROM password_history WHERE user_id = ?'), [user_id])
history = result.fetchall()

if history:
    for h in history:
        print(f"   ID: {h[0]}, Reason: {h[1]}, Date: {h[2]}")
else:
    print("   ⚠️  Pas d'historique trouvé")

conn.close()

# 3. Test authentication with different passwords
print("\n3️⃣  TEST D'AUTHENTIFICATION AVEC DIFFÉRENTS MOTS DE PASSE")
print("-" * 70)

test_passwords = [
    "password123",
    "test123",
    "immobilier@01",
    "Patrick123",
    "azertjilo123",
    "",
]

for test_pwd in test_passwords:
    try:
        is_valid = auth_service.verify_password(test_pwd, stored_hash)
        status = "✅ VALIDE" if is_valid else "❌ INVALIDE"
        print(f"   {status}: '{test_pwd}'")
    except Exception as e:
        print(f"   ⚠️  ERREUR: '{test_pwd}' - {e}")

# 4. Test bcrypt directly
print("\n4️⃣  TEST BCRYPT DIRECT")
print("-" * 70)

test_pwd = "password123"
encoded_test = test_pwd.encode('utf-8')
encoded_hash = stored_hash.encode('utf-8')

try:
    result = bcrypt.checkpw(encoded_test, encoded_hash)
    print(f"   bcrypt.checkpw('{test_pwd}', hash) = {result}")
except Exception as e:
    print(f"   ⚠️  ERREUR: {e}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
Si aucun mot de passe ne fonctionne, cela signifie que:
- Le mot de passe original lors de l'enregistrement est inconnu
- OU il y a un problème avec le hachage/vérification

Solution: Supprimer cet utilisateur et en créer un nouveau avec un mot de passe connu.
""")
print("="*70 + "\n")
