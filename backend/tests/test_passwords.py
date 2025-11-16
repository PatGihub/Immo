"""Tests for password handling and authentication"""
import pytest
from app.services.auth import auth_service, _truncate_password
from app.schemas import UserCreate

class TestPasswordValidation:
    """Test password validation"""
    
    def test_password_valid_simple(self):
        """Test simple valid password"""
        password = "simplePassword123"
        # Should hash without error
        hashed = auth_service.hash_password(password)
        assert hashed != password
    
    def test_password_valid_special_chars(self):
        """Test password with special characters"""
        password = "P@ssw0rd!#$%&*()"
        hashed = auth_service.hash_password(password)
        assert hashed != password
    
    def test_password_valid_unicode(self):
        """Test password with unicode characters"""
        password = "Pässwörd123ñ"
        hashed = auth_service.hash_password(password)
        assert hashed != password
    
    def test_password_valid_immobilier_example(self):
        """Test the example password from the project"""
        password = "immobilier@01"
        hashed = auth_service.hash_password(password)
        assert hashed != password
    
    def test_password_valid_complex(self):
        """Test complex password"""
        password = "MyP@ssw0rd!"
        hashed = auth_service.hash_password(password)
        assert hashed != password

class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password_basic(self):
        """Test basic password hashing"""
        password = "testPassword123"
        hashed = auth_service.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert "$2b$" in hashed  # bcrypt hash format
    
    def test_hash_password_different_results(self):
        """Test that hashing the same password produces different results"""
        password = "testPassword123"
        hashed1 = auth_service.hash_password(password)
        hashed2 = auth_service.hash_password(password)
        
        # Should be different due to salt
        assert hashed1 != hashed2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "testPassword123"
        hashed = auth_service.hash_password(password)
        
        is_valid = auth_service.verify_password(password, hashed)
        assert is_valid is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "testPassword123"
        wrong_password = "wrongPassword456"
        hashed = auth_service.hash_password(password)
        
        is_valid = auth_service.verify_password(wrong_password, hashed)
        assert is_valid is False
    
    def test_hash_and_verify_unicode_password(self):
        """Test hashing and verifying unicode password"""
        password = "Pässwörd123ñ"
        hashed = auth_service.hash_password(password)
        is_valid = auth_service.verify_password(password, hashed)
        
        assert is_valid is True
    
    def test_hash_and_verify_special_chars(self):
        """Test hashing and verifying password with special characters"""
        password = "P@ssw0rd!#$%&*()"
        hashed = auth_service.hash_password(password)
        is_valid = auth_service.verify_password(password, hashed)
        
        assert is_valid is True

class TestPasswordExamples:
    """Test specific password examples"""
    
    def test_immobilier_password(self):
        """Test the immobilier@01 password"""
        password = "immobilier@01"
        
        # Hash and verify
        hashed = auth_service.hash_password(password)
        is_valid = auth_service.verify_password(password, hashed)
        
        assert is_valid is True
    
    def test_complex_passwords(self):
        """Test various complex but valid passwords"""
        test_passwords = [
            "MyP@ssw0rd!",
            "SecurePass123#",
            "Déjà-vu_2024",
            "café@password.123",
            "!@#$%^&*()_+-=[]{}|;:,.<>?",
        ]
        
        for password in test_passwords:
            # Hash and verify
            hashed = auth_service.hash_password(password)
            is_valid = auth_service.verify_password(password, hashed)
            assert is_valid is True, f"Failed for password: {password}"

class TestEdgeCases:
    """Test edge cases for password handling"""
    
    def test_whitespace_password(self):
        """Test password with only whitespace"""
        password = "   "
        hashed = auth_service.hash_password(password)
        is_valid = auth_service.verify_password(password, hashed)
        assert is_valid is True
    
    def test_password_with_newlines(self):
        """Test password containing newlines"""
        password = "pass\nword\ntest"
        hashed = auth_service.hash_password(password)
        is_valid = auth_service.verify_password(password, hashed)
        assert is_valid is True
    
    def test_password_case_sensitive(self):
        """Test that password verification is case sensitive"""
        password = "TestPassword123"
        wrong_case = "testpassword123"
        hashed = auth_service.hash_password(password)
        
        is_valid_correct = auth_service.verify_password(password, hashed)
        is_valid_wrong = auth_service.verify_password(wrong_case, hashed)
        
        assert is_valid_correct is True
        assert is_valid_wrong is False
