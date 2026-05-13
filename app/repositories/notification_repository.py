"""Smart Guardian - Notification repository"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.notification import Notification


class NotificationRepository:
    """Data access layer for Notification model"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_by_user(self, user_id: int, limit: int = 50) -> List[Notification]:
        return self.db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).limit(limit).all()

    def get_unread_by_user(self, user_id: int) -> List[Notification]:
        return self.db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).order_by(Notification.created_at.desc()).all()

    def count_unread(self, user_id: int) -> int:
        return self.db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).count()

    def update(self, notification: Notification) -> Notification:
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_read(self, user_id: int) -> int:
        result = self.db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({"is_read": True})
        self.db.commit()
        return result
