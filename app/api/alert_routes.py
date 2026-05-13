"""Smart Guardian - Alert API routes"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/api/alerts", tags=['Alerts'])


@router.post("/", response_model=AlertResponse, status_code=201)
def create_alert(data: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert (from AI or device)"""
    service = AlertService(db)
    return service.create_alert(data)


@router.get("/user/{user_id}", response_model=List[AlertResponse])
def get_user_alerts(user_id: int, limit: int = Query(default=50, le=200), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get alerts for a user"""
    service = AlertService(db)
    return service.get_user_alerts(user_id, limit)


@router.get("/unread/{user_id}", response_model=List[AlertResponse])
def get_unread_alerts(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get unread alerts for a user"""
    service = AlertService(db)
    return service.get_unread(user_id)


@router.get("/critical", response_model=List[AlertResponse])
def get_critical_alerts(limit: int = Query(default=50, le=200), db: Session = Depends(get_db), current_user: User = Depends(require_role("admin", "doctor"))):
    """Get all unresolved critical alerts (admin/doctor)"""
    service = AlertService(db)
    return service.get_critical(limit)


@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, data: AlertUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Mark alert as read/resolved"""
    service = AlertService(db)
    return service.update_alert(alert_id, data)
