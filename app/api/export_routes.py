"""Smart Guardian - Export API routes"""

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import io
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.services.export_service import ExportService

router = APIRouter(prefix="/api/export", tags=["Data Export"])


@router.get("/alerts/csv/{user_id}")
def export_alerts_csv(user_id: int, days: Optional[int] = Query(default=None, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export alerts as CSV file"""
    service = ExportService(db)
    csv_data = service.export_alerts_csv(user_id, days)
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=alerts_user_{user_id}.csv"},
    )


@router.get("/alerts/json/{user_id}")
def export_alerts_json(user_id: int, days: Optional[int] = Query(default=None, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export alerts as JSON file"""
    service = ExportService(db)
    json_data = service.export_alerts_json(user_id, days)
    return JSONResponse(
        content=json.loads(json_data),
        headers={"Content-Disposition": f"attachment; filename=alerts_user_{user_id}.json"},
    )


@router.get("/sensors/csv/{user_id}")
def export_sensor_csv(user_id: int, days: Optional[int] = Query(default=None, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export sensor data as CSV file"""
    service = ExportService(db)
    csv_data = service.export_sensor_csv(user_id, days)
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=sensors_user_{user_id}.csv"},
    )


@router.get("/sensors/json/{user_id}")
def export_sensor_json(user_id: int, days: Optional[int] = Query(default=None, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export sensor data as JSON file"""
    service = ExportService(db)
    json_data = service.export_sensor_json(user_id, days)
    return JSONResponse(
        content=json.loads(json_data),
        headers={"Content-Disposition": f"attachment; filename=sensors_user_{user_id}.json"},
    )


@router.get("/full-report/{user_id}")
def export_full_report(user_id: int, days: Optional[int] = Query(default=None, le=365), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export full report with alerts and sensor data as JSON"""
    service = ExportService(db)
    json_data = service.export_full_report_json(user_id, days)
    return JSONResponse(
        content=json.loads(json_data),
        headers={"Content-Disposition": f"attachment; filename=report_user_{user_id}.json"},
    )
