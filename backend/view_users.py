#!/usr/bin/env python3
"""
Script pour visualiser les utilisateurs en base de données
Usage: python view_users.py [command] [args]

Commandes:
  all                  # Affiche tous les utilisateurs
  count                # Compte les utilisateurs
  find <username>      # Cherche un utilisateur
  delete <username>    # Supprime un utilisateur

Exemples:
  python view_users.py all
  python view_users.py count
  python view_users.py find patrick
  python view_users.py delete testuser
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, PasswordHistory
from app.config import settings

# Créer la connexion à la base de données
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def view_all_users():
    """Affiche tous les utilisateurs en base"""
    print("\n" + "="*80)
    print("VISUALISATION DE TOUS LES UTILISATEURS")
    print("="*80)
    
    users = db.query(User).all()
    
    if not users:
        print("\n⚠️  Aucun utilisateur en base de données\n")
        return
    
    print(f"\n📊 Total: {len(users)} utilisateur(s)\n")
    
    for idx, user in enumerate(users, 1):
        print("-" * 80)
        print(f"User #{idx}")
        print("-" * 80)
        print(f"  ID:        {user.id}")
        print(f"  Username:  {user.username}")
        print(f"  Email:     {user.email}")
        print(f"  Active:    {'✅' if user.is_active else '❌'}")
        print(f"  Created:   {user.created_at}")
        print(f"  Updated:   {user.updated_at}")
        
        # Afficher l'historique de mots de passe
        password_history = db.query(PasswordHistory).filter(
            PasswordHistory.user_id == user.id
        ).all()
        
        if password_history:
            print(f"\n  🔐 Password History ({len(password_history)} entry/entries):")
            for hist in password_history:
                print(f"    - Date: {hist.changed_at}")
                print(f"      Reason: {hist.reason}")
                print(f"      Hash: {hist.hashed_password[:40]}...")
                if hist.ip_address:
                    print(f"      IP: {hist.ip_address}")
        else:
            print(f"\n  🔐 Password History: Aucune entrée")
        
        print()
    
    print("="*80 + "\n")


def count_users():
    """Compte les utilisateurs"""
    count = db.query(User).count()
    print("\n" + "="*80)
    print(f"NOMBRE TOTAL D'UTILISATEURS: {count}")
    print("="*80 + "\n")
    return count


def find_user(username):
    """Cherche un utilisateur par username"""
    user = db.query(User).filter(User.username == username).first()
    
    print("\n" + "="*80)
    print(f"RECHERCHE: '{username}'")
    print("="*80)
    
    if user:
        print(f"\n✅ Utilisateur trouvé!")
        print(f"  ID:        {user.id}")
        print(f"  Username:  {user.username}")
        print(f"  Email:     {user.email}")
        print(f"  Active:    {'✅' if user.is_active else '❌'}")
        print(f"  Created:   {user.created_at}")
        print(f"  Updated:   {user.updated_at}")
    else:
        print(f"\n❌ Utilisateur '{username}' non trouvé")
        users = db.query(User).all()
        if users:
            print("\n📋 Utilisateurs disponibles:")
            for user in users:
                print(f"  - {user.username} ({user.email})")
        else:
            print("\n❌ Aucun utilisateur en base")
    
    print("="*80 + "\n")


def delete_user(username):
    """Supprime un utilisateur"""
    user = db.query(User).filter(User.username == username).first()
    
    print("\n" + "="*80)
    print(f"SUPPRESSION D'UTILISATEUR: '{username}'")
    print("="*80)
    
    if user:
        db.delete(user)
        db.commit()
        print(f"\n✅ Utilisateur '{username}' supprimé!")
    else:
        print(f"\n❌ Utilisateur '{username}' non trouvé")
    
    print("="*80 + "\n")


def main():
    """Fonction principale"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    try:
        if command == "all":
            view_all_users()
        elif command == "count":
            count_users()
        elif command == "find":
            if len(sys.argv) < 3:
                print("❌ Usage: python view_users.py find <username>\n")
                sys.exit(1)
            find_user(sys.argv[2])
        elif command == "delete":
            if len(sys.argv) < 3:
                print("❌ Usage: python view_users.py delete <username>\n")
                sys.exit(1)
            delete_user(sys.argv[2])
        else:
            print(f"❌ Commande inconnue: {command}\n")
            print(__doc__)
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
