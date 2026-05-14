"""Training pipeline schemas."""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class TrainingRequest(BaseModel):
    epochs: int = Field(50, ge=1, le=500)
    batch_size: int = Field(32, ge=8, le=256)
    learning_rate: float = Field(0.001, ge=0.0001, le=0.1)
    augmentation: bool = Field(True, description="Enable data augmentation")
    noise_level: float = Field(0.05, ge=0.0, le=0.3)
    validation_split: float = Field(0.2, ge=0.1, le=0.5)

class TrainingStatusResponse(BaseModel):
    is_training: bool
    current_epoch: int = 0
    total_epochs: int = 0
    loss: Optional[float] = None
    accuracy: Optional[float] = None
    val_loss: Optional[float] = None
    val_accuracy: Optional[float] = None

class ModelVersionResponse(BaseModel):
    version: str
    created_at: str
    accuracy: Optional[float] = None
    loss: Optional[float] = None
    is_active: bool = False

class TrainingResultResponse(BaseModel):
    version: str
    epochs: int
    final_loss: float
    final_accuracy: float
    final_val_loss: Optional[float] = None
    final_val_accuracy: Optional[float] = None

    augmentation_applied: bool = False
    training_samples: int = 0
    validation_samples: int = 0
