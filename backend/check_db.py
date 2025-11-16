#!/usr/bin/env python3
"""Check database contents"""

from sqlalchemy import create_engine, text

# Create engine
engine = create_engine("sqlite:///./immobilier.db")

print("\n" + "="*60)
print("CHECKING DATABASE CONTENTS")
print("="*60)

# Check users table
print("\n📋 USERS IN DATABASE:")
print("-" * 60)
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, username, email, is_active, created_at FROM user LIMIT 20"))
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(f"  ID: {row[0]}, Username: {row[1]}, Email: {row[2]}, Active: {row[3]}, Created: {row[4]}")
        else:
            print("  ⚠️  No users found in database!")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Check password history
print("\n📋 PASSWORD HISTORY:")
print("-" * 60)
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, user_id, changed_at, reason FROM password_history LIMIT 10"))
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(f"  ID: {row[0]}, User ID: {row[1]}, Changed: {row[2]}, Reason: {row[3]}")
        else:
            print("  ⚠️  No password history found!")
except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("END OF CHECK")
print("="*60 + "\n")
