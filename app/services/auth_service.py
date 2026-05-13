"""Smart Guardian - Authentication service"""

import logging
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, LoginRequest, TokenResponse, UserResponse

logger = logging.getLogger("smart-guardian")


class AuthService:
    """Business logic for authentication"""

    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        if self.user_repo.get_by_username(user_data.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            role=user_data.role,
        )
        user = self.user_repo.create(user)
        logger.info("User registered: %s", user.username)
        return UserResponse.model_validate(user)

    def login(self, login_data: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_by_email(login_data.username)
        if not user:
            user = self.user_repo.get_by_username(login_data.username)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account deactivated")
        access_token = create_access_token({"sub": user.username, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.username})
        logger.info("User logged in: %s", user.username)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user = self.user_repo.get_by_username(payload.get("sub"))
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        new_access = create_access_token({"sub": user.username, "role": user.role})
        new_refresh = create_refresh_token({"sub": user.username})
        return TokenResponse(access_token=new_access, refresh_token=new_refresh)
