"""Smart Guardian - Dashboard & Analytics API routes"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.services.dashboard_service import DashboardService
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard & Analytics"])


@router.get("/admin-stats")
def get_admin_stats(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Get global admin dashboard statistics"""
    service = DashboardService(db)
    return service.get_admin_stats()


@router.get("/patient-stats/{user_id}")
def get_patient_stats(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get patient-specific dashboard statistics"""
    service = DashboardService(db)
    return service.get_patient_stats(user_id)


@router.get("/alert-trend")
def get_alert_trend(days: int = Query(default=30, le=365), db: Session = Depends(get_db), current_user: User = Depends(require_role("admin", "doctor"))):
    """Get alert count trend over last N days"""
    service = DashboardService(db)
    return service.get_alert_trend(days)


@router.get("/patient-alert-trend/{user_id}")
def get_patient_alert_trend(user_id: int, days: int = Query(default=30, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get alert trend for a specific patient"""
    service = DashboardService(db)
    return service.get_patient_alert_trend(user_id, days)


@router.get("/severity-distribution")
def get_severity_distribution(user_id: int = None, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin", "doctor"))):
    """Get alert severity distribution"""
    service = DashboardService(db)
    return service.get_severity_distribution(user_id)


@router.get("/seizure-frequency/{user_id}")
def get_seizure_frequency(user_id: int, days: int = Query(default=90, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get seizure frequency stats for a patient"""
    service = AnalyticsService(db)
    return service.get_seizure_frequency(user_id, days)


@router.get("/seizure-hourly/{user_id}")
def get_hourly_distribution(user_id: int, days: int = Query(default=90, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get hourly seizure distribution"""
    service = AnalyticsService(db)
    return service.get_hourly_distribution(user_id, days)


@router.get("/seizure-weekly/{user_id}")
def get_weekly_distribution(user_id: int, days: int = Query(default=180, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get day-of-week seizure distribution"""
    service = AnalyticsService(db)
    return service.get_weekly_distribution(user_id, days)


@router.get("/seizure-vitals/{user_id}")
def get_vitals_during_seizures(user_id: int, limit: int = Query(default=20, le=100), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get vitals data during seizure events"""
    service = AnalyticsService(db)
    return service.get_vitals_during_seizures(user_id, limit)


@router.get("/seizure-summary/{user_id}")
def get_seizure_summary(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get comprehensive seizure analytics summary"""
    service = AnalyticsService(db)
    return service.get_seizure_summary(user_id)
