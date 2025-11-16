#!/usr/bin/env python3
"""
Script pour supprimer TOUS les utilisateurs de la base de données
⚠️ ATTENTION: Cette action est irréversible!

Usage: python delete_all_users.py [confirm]

Exemples:
  python delete_all_users.py          # Affiche le nombre d'utilisateurs et demande confirmation
  python delete_all_users.py confirm  # Supprime directement sans confirmation
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


def delete_all_users(force=False):
    """Supprime tous les utilisateurs de la base"""
    
    # Compter les utilisateurs
    count = db.query(User).count()
    
    print("\n" + "="*80)
    print("⚠️  SUPPRESSION DE TOUS LES UTILISATEURS")
    print("="*80)
    
    if count == 0:
        print("\n❌ Aucun utilisateur en base de données\n")
        return
    
    print(f"\n⚠️  Il y a {count} utilisateur(s) en base:")
    
    # Afficher les utilisateurs
    users = db.query(User).all()
    for idx, user in enumerate(users, 1):
        print(f"  {idx}. {user.username} ({user.email})")
    
    print("\n" + "="*80)
    
    if not force:
        # Demander confirmation
        response = input(f"\n⚠️  Êtes-vous ABSOLUMENT sûr de vouloir supprimer ces {count} utilisateur(s)?\n   Type 'DELETE' pour confirmer: ").strip()
        
        if response != "DELETE":
            print("\n❌ Opération annulée\n")
            return
    
    # Supprimer tous les utilisateurs (PasswordHistory sera supprimé en cascade)
    try:
        db.query(User).delete()
        db.commit()
        print(f"\n✅ {count} utilisateur(s) supprimé(s) avec succès!")
        print("✅ L'historique des mots de passe a également été supprimé")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur lors de la suppression: {e}")
    
    print("="*80 + "\n")


def main():
    """Fonction principale"""
    force_delete = len(sys.argv) > 1 and sys.argv[1].lower() == "confirm"
    
    try:
        delete_all_users(force=force_delete)
    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
