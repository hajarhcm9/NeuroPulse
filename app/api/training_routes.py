"""Smart Guardian - Model Training API routes (admin only)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User
from app.schemas.training import (
    TrainingRequest,
    TrainingStatusResponse,
    TrainingResultResponse,
    ModelVersionResponse,
)
from app.services.training_service import training_service

router = APIRouter(prefix="/api/training", tags=["Model Training"])


@router.post("/start")
def start_training(config: TrainingRequest, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Start model training with specified configuration (admin only)."""
    result = training_service.start_training(config.model_dump())
    if "error" in result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result["error"])
    return result


@router.get("/status", response_model=TrainingStatusResponse)
def get_training_status(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Get current training status (admin only)."""
    s = training_service.get_status()
    return TrainingStatusResponse(**s)


@router.get("/versions", response_model=list[ModelVersionResponse])
def list_model_versions(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin", "doctor"))):
    """List all saved model versions (admin/doctor)."""
    return training_service.list_versions()


@router.post("/activate/{version}")
def activate_model_version(version: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Activate a specific model version (admin only)."""
    success = training_service.activate_version(version)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found or model file missing")
    return {"message": "Model version activated", "version": version}


@router.delete("/versions/{version}")
def delete_model_version(version: str, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    """Delete a saved model version (admin only)."""
    success = training_service.delete_version(version)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Version not found or is active")
    return {"message": "Model version deleted", "version": version}