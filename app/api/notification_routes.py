"""Smart Guardian - Notification API routes"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationResponse, NotificationUpdate
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/api/notifications", tags=['Notifications'])


@router.post("/", response_model=NotificationResponse, status_code=201)
def create_notification(data: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin", "doctor"))):
    """Create and dispatch a notification (admin/doctor)"""
    service = NotificationService(db)
    return service.create_notification(data)


@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_user_notifications(user_id: int, limit: int = Query(default=50, le=200), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get notifications for a user"""
    service = NotificationService(db)
    return service.get_user_notifications(user_id, limit)


@router.get("/unread/{user_id}", response_model=List[NotificationResponse])
def get_unread_notifications(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get unread notifications for a user"""
    service = NotificationService(db)
    return service.get_unread(user_id)


@router.get("/unread-count/{user_id}")
def get_unread_count(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get unread notification count"""
    service = NotificationService(db)
    return {"user_id": user_id, "unread_count": service.get_unread_count(user_id)}


@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Mark a notification as read"""
    service = NotificationService(db)
    return service.mark_read(notification_id)


@router.put("/mark-all-read/{user_id}")
def mark_all_read(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Mark all notifications as read for a user"""
    service = NotificationService(db)
    return service.mark_all_read(user_id)
