"""Smart Guardian - AI Prediction API routes"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.schemas.prediction import PredictionRequest, PredictionResponse, ModelInfoResponse, BatchPredictionRequest, BatchPredictionResponse
from app.services.seizure_detection_service import SeizureDetectionService
from app.services.model_service import model_service

router = APIRouter(prefix="/api/predictions", tags=["AI Predictions"])


@router.post("/analyze", response_model=PredictionResponse)
async def analyze_sensor_data(data: PredictionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Analyze sensor data for seizure detection"""
    service = SeizureDetectionService(db)
    return await service.analyze(data)


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_analyze(data: BatchPredictionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Batch analyze multiple sensor data points"""
    service = SeizureDetectionService(db)
    return await service.batch_analyze(data)


@router.get("/model-info", response_model=ModelInfoResponse)
def get_model_info(current_user: User = Depends(require_role("admin", "doctor"))):
    """Get AI model information (admin/doctor only)"""
    return model_service.get_model_info()


@router.post("/reload-model")
def reload_model(current_user: User = Depends(require_role("admin"))):
    """Reload the AI model (admin only)"""
    model_service._model = None
    model_service.load_model()
    return {"message": "Model reloaded", "is_loaded": model_service.is_loaded}
