"""Smart Guardian - User API routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/users", tags=['Users'])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(user_data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update current user profile"""
    if user_data.email is not None:
        current_user.email = user_data.email
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name
    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name
    if user_data.phone is not None:
        current_user.phone = user_data.phone
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db)
    repo.update(current_user)
    return current_user


@router.get("/", response_model=list[UserResponse])
def list_users(current_user: User = Depends(require_role("admin", "doctor")), db: Session = Depends(get_db)):
    """List all users (admin/doctor only)"""
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db)
    return repo.db.query(User).all()
