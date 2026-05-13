"""Smart Guardian - Sensor data API routes"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.sensor_data import SensorDataCreate, SensorDataResponse
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/api/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorDataResponse, status_code=201)
def submit_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Submit sensor data from bracelet"""
    service = SensorService(db)
    return service.store_sensor_data(data)


@router.get("/user/{user_id}", response_model=List[SensorDataResponse])
def get_user_sensor_data(user_id: int, limit: int = Query(default=100, le=500), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get sensor data for a specific user"""
    service = SensorService(db)
    return service.get_user_data(user_id, limit)


@router.get("/device/{device_id}", response_model=List[SensorDataResponse])
def get_device_sensor_data(device_id: str, limit: int = Query(default=100, le=500), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get sensor data for a specific device"""
    service = SensorService(db)
    return service.get_device_data(device_id, limit)


@router.get("/latest/{user_id}", response_model=SensorDataResponse)
def get_latest_sensor_data(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get latest sensor reading for a user"""
    service = SensorService(db)
    return service.get_latest(user_id)
