from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List

# ==================== Auth Schemas ====================

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    user: "UserResponse"

class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None

# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """User creation schema"""
    password: str

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        if len(v) > 72:
            raise ValueError("Password cannot be longer than 72 characters.")
        return v

class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ==================== Password History Schemas ====================

class PasswordHistoryItem(BaseModel):
    """Single password history item"""
    changed_at: datetime
    reason: Optional[str]
    ip_address: Optional[str]

class PasswordHistoryResponse(BaseModel):
    """Password history response"""
    username: str
    history: List[PasswordHistoryItem]

# ==================== Property Schemas ====================

class PropertyBase(BaseModel):
    """Base property schema"""
    title: str
    description: Optional[str] = None
    price: int
    location: str
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[int] = None

class PropertyCreate(PropertyBase):
    """Property creation schema"""
    pass

class PropertyUpdate(BaseModel):
    """Property update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    location: Optional[str] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[int] = None

class PropertyResponse(PropertyBase):
    """Property response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

