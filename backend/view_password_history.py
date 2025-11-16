#!/usr/bin/env python3
"""Check password history in database"""

from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///./immobilier.db')
conn = engine.connect()

print("\n" + "="*70)
print("HISTORIQUE COMPLET DES MOTS DE PASSE")
print("="*70)

# Get password history with hashed password
result = conn.execute(text('SELECT id, user_id, hashed_password, reason, changed_at FROM password_history'))
rows = result.fetchall()

print(f"\nNombre d'entrées: {len(rows)}\n")

for row in rows:
    print(f"ID: {row[0]}")
    print(f"User ID: {row[1]}")
    print(f"Reason: {row[3]}")
    print(f"Changed at: {row[4]}")
    print(f"Hashed password:")
    print(f"  {row[2]}")
    print()

conn.close()
print("="*70)
