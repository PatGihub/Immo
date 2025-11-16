"""Tests for authentication endpoints"""
import pytest
from conftest import client, db

class TestRegistrationEndpoint:
    """Test user registration endpoint"""
    
    def test_register_valid_user(self, client):
        """Test registration with valid credentials"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testPassword123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "hashed_password" not in data  # Password should not be exposed
    
    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username"""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test1@example.com",
                "password": "testPassword123"
            }
        )
        
        # Second registration with same username
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test2@example.com",
                "password": "testPassword456"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser1",
                "email": "test@example.com",
                "password": "testPassword123"
            }
        )
        
        # Second registration with same email
        response = client.post(
            "/api/auth/register",
            json={
                "username": "testuser2",
                "email": "test@example.com",
                "password": "testPassword456"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_register_immobilier_password(self, client):
        """Test registration with immobilier@01 password"""
        response = client.post(
            "/api/auth/register",
            json={
                "username": "immobilier_user",
                "email": "immobilier@test.com",
                "password": "immobilier@01"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "immobilier_user"
        assert data["email"] == "immobilier@test.com"

class TestLoginEndpoint:
    """Test user login endpoint"""
    
    def test_login_valid_credentials(self, client):
        """Test login with valid credentials"""
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testPassword123"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testPassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["username"] == "testuser"
    
    def test_login_invalid_username(self, client):
        """Test login with non-existent username"""
        response = client.post(
            "/api/auth/login",
            json={
                "username": "nonexistent",
                "password": "anyPassword123"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client):
        """Test login with wrong password"""
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "correctPassword123"
            }
        )
        
        # Login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "wrongPassword456"
            }
        )
        
        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]
    
    def test_login_case_sensitive_username(self, client):
        """Test login with different case username"""
        # Register with lowercase
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testPassword123"
            }
        )
        
        # Try login with uppercase
        response = client.post(
            "/api/auth/login",
            json={
                "username": "TESTUSER",
                "password": "testPassword123"
            }
        )
        
        # Should fail (usernames are case-sensitive)
        assert response.status_code == 401

class TestMeEndpoint:
    """Test get current user endpoint"""
    
    def test_get_current_user_authenticated(self, client):
        """Test getting current user with valid token"""
        # Register and login
        client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "testPassword123"
            }
        )
        
        login_response = client.post(
            "/api/auth/login",
            json={
                "username": "testuser",
                "password": "testPassword123"
            }
        )
        
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        assert "Missing authorization header" in response.json()["detail"]
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
