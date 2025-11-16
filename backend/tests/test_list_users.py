#!/usr/bin/env python3
"""
Script pour lister tous les utilisateurs en base de données
Utile pour vérifier l'état de la base après les tests
"""

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from conftest import client, db
from app.models import User
from app.services.password import PasswordHistoryService


class TestListUsers:
    """Tests pour lister et afficher les utilisateurs en base"""
    
    def test_list_all_users(self, db: Session):
        """
        Affiche tous les utilisateurs actuellement en base de données
        avec leurs informations et historique de mots de passe
        """
        print("\n" + "="*80)
        print("LISTE DE TOUS LES UTILISATEURS EN BASE DE DONNÉES")
        print("="*80)
        
        # Récupérer tous les utilisateurs
        users = db.query(User).all()
        
        if not users:
            print("\n⚠️  Aucun utilisateur en base de données")
            return
        
        print(f"\n📊 Total: {len(users)} utilisateur(s)\n")
        
        # Afficher chaque utilisateur
        for idx, user in enumerate(users, 1):
            print("-" * 80)
            print(f"User #{idx}")
            print("-" * 80)
            print(f"  ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Active: {user.is_active}")
            print(f"  Created At: {user.created_at}")
            print(f"  Updated At: {user.updated_at}")
            
            # Afficher l'historique de mots de passe
            password_history = PasswordHistoryService.get_password_history(db, user.id)
            if password_history:
                print(f"\n  🔐 Password History ({len(password_history)} entry/entries):")
                for hist in password_history:
                    print(f"    - Date: {hist.changed_at}")
                    print(f"      Reason: {hist.reason}")
                    print(f"      Hash: {hist.hashed_password[:30]}...")
                    if hist.ip_address:
                        print(f"      IP: {hist.ip_address}")
            else:
                print(f"\n  🔐 Password History: Aucune entrée")
            
            print()
        
        print("="*80)
    
    def test_count_users(self, db: Session):
        """Compte et affiche le nombre d'utilisateurs"""
        user_count = db.query(User).count()
        
        print("\n" + "="*80)
        print(f"NOMBRE TOTAL D'UTILISATEURS: {user_count}")
        print("="*80 + "\n")
        
        assert user_count >= 0, "Le nombre d'utilisateurs ne peut pas être négatif"
    
    def test_find_user_by_username(self, db: Session):
        """
        Test pour chercher un utilisateur spécifique par username
        Modifier 'testuser' par le username que tu cherches
        """
        search_username = "testuser"
        
        user = db.query(User).filter(User.username == search_username).first()
        
        print("\n" + "="*80)
        print(f"RECHERCHE D'UTILISATEUR: '{search_username}'")
        print("="*80)
        
        if user:
            print(f"\n✅ Utilisateur trouvé!")
            print(f"  ID: {user.id}")
            print(f"  Username: {user.username}")
            print(f"  Email: {user.email}")
            print(f"  Active: {user.is_active}")
            print(f"  Created At: {user.created_at}")
        else:
            print(f"\n❌ Utilisateur '{search_username}' non trouvé en base")
            print("\n📋 Utilisateurs disponibles:")
            users = db.query(User).all()
            for user in users:
                print(f"  - {user.username} ({user.email})")
        
        print("="*80 + "\n")
    
    def test_delete_user_by_username(self, db: Session):
        """
        Test pour supprimer un utilisateur spécifique
        ATTENTION: Modifie la base de données!
        Décommenter et modifier 'username_to_delete' pour utiliser
        """
        # DÉCOMMENTER POUR UTILISER:
        # username_to_delete = "testuser"
        # 
        # user = db.query(User).filter(User.username == username_to_delete).first()
        # if user:
        #     db.delete(user)
        #     db.commit()
        #     print(f"\n✅ Utilisateur '{username_to_delete}' supprimé")
        # else:
        #     print(f"\n❌ Utilisateur '{username_to_delete}' non trouvé")
        
        print("\n⚠️  Cette fonction est désactivée par défaut")
        print("Pour supprimer un utilisateur, décommenter le code dans le test")
    
    def test_export_users_json(self, db: Session):
        """
        Export tous les utilisateurs au format JSON
        Sauvegarde dans un fichier pour inspection
        """
        import json
        from datetime import datetime
        
        users = db.query(User).all()
        
        users_data = []
        for user in users:
            password_history = PasswordHistoryService.get_password_history(db, user.id)
            users_data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "password_history_count": len(password_history),
                "password_history": [
                    {
                        "changed_at": hist.changed_at.isoformat() if hist.changed_at else None,
                        "reason": hist.reason,
                        "hash": hist.hashed_password[:30] + "...",
                        "ip_address": hist.ip_address
                    }
                    for hist in password_history
                ]
            })
        
        # Sauvegarder dans un fichier
        filename = f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print(f"✅ Export sauvegardé: {filename}")
        print(f"   Total: {len(users_data)} utilisateur(s)")
        print("="*80 + "\n")


if __name__ == "__main__":
    """
    Pour exécuter ces tests :
    cd backend
    python -m pytest tests/test_list_users.py -v -s
    
    Pour un test spécifique :
    python -m pytest tests/test_list_users.py::TestListUsers::test_list_all_users -v -s
    """
    pytest.main([__file__, "-v", "-s"])
