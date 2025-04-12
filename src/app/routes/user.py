from sqlalchemy.orm import Session
from fastapi import Depends, Request, File, UploadFile
from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.current_user import get_current_user
from app.response.schemas import User
from app.controllers.user import UserController
from app.database.db import get_db
from app.services.upload_file import UploadFileService
from app.config.config import settings

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
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, user.name)

    user.avatar = avatar_url
    user_controller = UserController(db)
    
    return await user_controller.update_user(user.id, user)