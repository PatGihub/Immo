import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings - Simple config without Pydantic"""
    app_name: str = "Immobilier API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    api_version: str = "0.0.1"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./immobilier.db")
    
    # CORS
    allowed_origins: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
