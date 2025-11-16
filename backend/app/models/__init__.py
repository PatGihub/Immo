from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PasswordHistory(Base):
    """Password history model - tracks password changes"""
    __tablename__ = "password_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String(50), nullable=True)  # Optional: track IP of password change
    reason = Column(String(100), nullable=True)  # e.g., "registration", "password_reset", "manual_change"

class Property(Base):
    """Property/Immobilier model"""
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    price = Column(Integer, nullable=False)
    location = Column(String(200), nullable=False)
    rooms = Column(Integer)
    bathrooms = Column(Integer)
    area = Column(Integer)  # in m²
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
