from sqlalchemy.orm import Session
from fastapi import Depends, Request, File, UploadFile, HTTPException, status, APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.current_user import get_current_user
from app.response.schemas import User
from app.controllers.user import UserController
from app.database.db import get_db
from app.services.upload_file import UploadFileService
from app.config.config import settings
from app.response.schemas import UserUpdate
from app.services.auth import Hash
from app.database.models import UserRole

router = APIRouter(prefix="/users", tags=["users"])
"""
API router for user endpoints.
"""

limiter = Limiter(key_func=get_remote_address)
"""
Limiter for rate limiting user requests.
"""


@router.get("/me", response_model=User, status_code=200)
@limiter.limit("10/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    """
    Get the current user.

    This endpoint returns the current user.

    Args:
        request (Request): The request.
        user (User): The current user.

    Returns:
        User: The current user.
    """
    return user


@router.patch("/avatar", response_model=User, status_code=200)
@limiter.limit("10/minute")
async def update_user(
    request: Request,
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's avatar.

    This endpoint updates the user's avatar.

    Args:
        request (Request): The request.
        file (UploadFile): The avatar file.
        user (User): The current user.
        db (Session): The database session.

    Returns:
        User: The updated user.
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, user.name)

    new_avatar = UserUpdate(avatar=avatar_url)
    user_controller = UserController(db)
    
    return await user_controller.update_user(user.id, new_avatar)

@router.patch("/reset", response_model=User, status_code=200)
@limiter.limit("3/minute")
async def update_user_password(
    request: Request,
    password: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's password.

    This endpoint updates the user's password.

    Args:
        request (Request): The request.
        user (User): The current user.
        db (Session): The database session.

    Returns:
        User: The updated user.
    """
    user_controller = UserController(db)
    hashed_password = Hash().get_password_hash(password)
    new_password = UserUpdate(password=hashed_password)
    
    return await user_controller.update_user(user.id, new_password)

@router.patch("/update_role", response_model=User, status_code=200)
@limiter.limit("3/minute")
async def update_user_role(
    request: Request,
    role: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's role.

    This endpoint updates the user's role.

    Args:
        request (Request): The request.
        user (User): The current user.
        db (Session): The database session.

    Returns:
        User: The updated user.
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    user_controller = UserController(db)
    new_role = UserUpdate(role=role)
    
    return await user_controller.update_user(user.id, new_role)