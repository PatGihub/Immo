"""Service for managing password history"""
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import PasswordHistory, User

logger = logging.getLogger("auth")

class PasswordHistoryService:
    """Service for managing password change history"""
    
    @staticmethod
    def record_password_change(
        db: Session,
        user_id: int,
        hashed_password: str,
        reason: str = "manual_change",
        ip_address: Optional[str] = None
    ) -> PasswordHistory:
        """Record a password change in history"""
        try:
            history = PasswordHistory(
                user_id=user_id,
                hashed_password=hashed_password,
                reason=reason,
                ip_address=ip_address,
                changed_at=datetime.utcnow()
            )
            db.add(history)
            db.commit()
            db.refresh(history)
            logger.info(f"Password change recorded for user_id {user_id}: {reason}")
            return history
        except Exception as e:
            logger.error(f"Error recording password change: {str(e)}", exc_info=True)
            db.rollback()
            raise
    
    @staticmethod
    def get_password_history(db: Session, user_id: int, limit: int = 10) -> list:
        """Get password history for a user"""
        try:
            history = db.query(PasswordHistory)\
                .filter(PasswordHistory.user_id == user_id)\
                .order_by(PasswordHistory.changed_at.desc())\
                .limit(limit)\
                .all()
            return history
        except Exception as e:
            logger.error(f"Error fetching password history: {str(e)}", exc_info=True)
            return []
    
    @staticmethod
    def get_latest_password(db: Session, user_id: int) -> Optional[PasswordHistory]:
        """Get the latest password change for a user"""
        try:
            latest = db.query(PasswordHistory)\
                .filter(PasswordHistory.user_id == user_id)\
                .order_by(PasswordHistory.changed_at.desc())\
                .first()
            return latest
        except Exception as e:
            logger.error(f"Error fetching latest password: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def clear_password_history(db: Session, user_id: int) -> int:
        """Clear password history for a user (careful!)"""
        try:
            deleted = db.query(PasswordHistory)\
                .filter(PasswordHistory.user_id == user_id)\
                .delete()
            db.commit()
            logger.warning(f"Password history cleared for user_id {user_id}: {deleted} records deleted")
            return deleted
        except Exception as e:
            logger.error(f"Error clearing password history: {str(e)}", exc_info=True)
            db.rollback()
            raise

password_history_service = PasswordHistoryService()
