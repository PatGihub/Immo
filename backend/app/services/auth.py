from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from app.config import settings
import logging

logger = logging.getLogger("auth")

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """
    Safely truncate password to max bytes in UTF-8.
    This is REQUIRED because bcrypt cannot handle passwords > 72 bytes.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= max_bytes:
        return password
    
    # Truncate at max_bytes and safely decode, handling incomplete UTF-8 sequences
    truncated = password_bytes[:max_bytes]
    while truncated:
        try:
            return truncated.decode('utf-8')
        except UnicodeDecodeError:
            # Remove last byte if it's part of incomplete UTF-8 sequence
            truncated = truncated[:-1]
    
    return ""  # Fallback (should never happen with valid UTF-8)

class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt directly"""
        try:
            # CRITICAL: Truncate to 72 bytes BEFORE bcrypt sees it
            password = _truncate_password(password)
            # bcrypt.hashpw returns bytes, decode to string for storage
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            logger.debug("Password hashed successfully")
            return hashed.decode('utf-8')
        except Exception as e:
            import traceback
            logger.error(
                f"PASSWORD HASH ERROR - Type: {type(e).__name__}\n"
                f"Message: {str(e)}\n"
                f"Stack Trace:\n{traceback.format_exc()}",
                exc_info=True
            )
            raise
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            # CRITICAL: Truncate to 72 bytes BEFORE bcrypt sees it
            plain_password = _truncate_password(plain_password)
            # bcrypt.checkpw expects both arguments as bytes
            is_valid = bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
            if is_valid:
                logger.debug("Password verification: success")
            else:
                logger.debug("Password verification: failed - hash mismatch")
            return is_valid
        except Exception as e:
            logger.error(f"Password verification error: {type(e).__name__}: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.algorithm
        )
        logger.info(f"JWT token created for user: {data.get('sub')}")
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            logger.debug(f"Token verified for user: {payload.get('sub')}")
            return payload
        except JWTError as e:
            import traceback
            logger.warning(
                f"TOKEN VERIFICATION ERROR - Type: {type(e).__name__}\n"
                f"Message: {str(e)}\n"
                f"Stack Trace:\n{traceback.format_exc()}"
            )
            return None
        except Exception as e:
            import traceback
            logger.error(
                f"UNEXPECTED TOKEN ERROR - Type: {type(e).__name__}\n"
                f"Message: {str(e)}\n"
                f"Stack Trace:\n{traceback.format_exc()}",
                exc_info=True
            )
            return None

auth_service = AuthService()
