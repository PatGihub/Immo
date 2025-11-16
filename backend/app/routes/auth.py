from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
import logging

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.auth import auth_service
from app.services.password import password_history_service

logger = logging.getLogger("auth")
router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        logger.info(f"Register attempt for username: {user_in.username}, email: {user_in.email}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == user_in.username) | (User.email == user_in.email)
        ).first()
        
        if existing_user:
            logger.warning(f"Registration failed: Username or email already exists - {user_in.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create new user
        hashed_password = auth_service.hash_password(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Record password change in history
        client_ip = request.client.host if request.client else "unknown"
        password_history_service.record_password_change(
            db=db,
            user_id=db_user.id,
            hashed_password=hashed_password,
            reason="registration",
            ip_address=client_ip
        )
        
        logger.info(f"User registered successfully: {user_in.username} (id: {db_user.id})")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        # Log l'exception complète avec stack trace et message détaillé
        import traceback
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "username": user_in.username,
            "stacktrace": traceback.format_exc()
        }
        logger.error(
            f"REGISTRATION ERROR - Type: {error_details['error_type']}\n"
            f"Message: {error_details['error_message']}\n"
            f"User: {error_details['username']}\n"
            f"Stack Trace:\n{error_details['stacktrace']}",
            exc_info=True  # Inclut aussi le stack trace automatique
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    try:
        logger.info(f"Login attempt for username: {login_data.username}")
        
        # Find user
        user = db.query(User).filter(User.username == login_data.username).first()
        
        if not user or not auth_service.verify_password(login_data.password, user.hashed_password):
            logger.warning(f"Login failed: Invalid credentials for username: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create token
        access_token_expires = timedelta(minutes=30)
        access_token = auth_service.create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in successfully: {user.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log l'exception complète avec stack trace et message détaillé
        import traceback
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "username": login_data.username,
            "stacktrace": traceback.format_exc()
        }
        logger.error(
            f"LOGIN ERROR - Type: {error_details['error_type']}\n"
            f"Message: {error_details['error_message']}\n"
            f"User: {error_details['username']}\n"
            f"Stack Trace:\n{error_details['stacktrace']}",
            exc_info=True  # Inclut aussi le stack trace automatique
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.post("/logout")
def logout():
    """Logout (client-side token invalidation)"""
    logger.info("User logged out")
    return {"message": "Logged out successfully"}

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Get current authenticated user from Authorization header"""
    if not authorization:
        logger.warning("Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.warning("Invalid authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    payload = auth_service.verify_token(token)
    
    if payload is None:
        logger.warning("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        logger.warning("Token missing username")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        logger.warning(f"User not found: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    try:
        logger.debug(f"Fetching current user info: {current_user.username}")
        return current_user
    except Exception as e:
        # Log l'exception avec stack trace détaillé
        import traceback
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_id": current_user.id if hasattr(current_user, 'id') else 'unknown',
            "stacktrace": traceback.format_exc()
        }
        logger.error(
            f"GET_ME ERROR - Type: {error_details['error_type']}\n"
            f"Message: {error_details['error_message']}\n"
            f"User ID: {error_details['user_id']}\n"
            f"Stack Trace:\n{error_details['stacktrace']}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user: {str(e)}"
        )

@router.get("/password-history")
def get_password_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get password change history for current user"""
    try:
        logger.info(f"Fetching password history for user: {current_user.username}")
        history = password_history_service.get_password_history(db, current_user.id, limit)
        
        # Return only non-sensitive info (no hashes, just metadata)
        return {
            "username": current_user.username,
            "history": [
                {
                    "changed_at": h.changed_at.isoformat(),
                    "reason": h.reason,
                    "ip_address": h.ip_address
                }
                for h in history
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching password history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching password history: {str(e)}"
        )
