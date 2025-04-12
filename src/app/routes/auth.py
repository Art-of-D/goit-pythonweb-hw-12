from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    BackgroundTasks,
    Request,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database.db import get_db
from app.response.schemas import UserCreate, Token, ConfirmResponse
from app.services.auth import create_access_token
from app.controllers.user import UserController
from app.services.auth import Hash
from app.services.email import send_email
from app.services.auth import get_email_from_token

router = APIRouter(prefix="/auth", tags=["auth"])
"""
API router for authentication endpoints.
"""

limiter = Limiter(key_func=get_remote_address)
"""
Limiter for rate limiting authentication requests.
"""


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login a user.

    This endpoint authenticates a user and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.
        db (Session): The database session.

    Returns:
        Token: The access token.
    """
    user_service = UserController(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not confirmed",
        )
    access_token = await create_access_token(data={"id": user.id, "sub": user.email, "name": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register", response_model=UserCreate, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    This endpoint creates a new user and sends a confirmation email.

    Args:
        user_data (UserCreate): The user data.
        background_tasks (BackgroundTasks): The background tasks.
        request (Request): The request.
        db (Session): The database session.

    Returns:
        UserCreate: The created user.
    """
    user_service = UserController(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    username_user = await user_service.get_user_by_username(user_data.name)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        send_email, new_user.email, new_user.name, request.base_url
    )
    return new_user


@router.get("/confirm_email/{token}", response_model=ConfirmResponse, status_code=201)
@limiter.limit("10/minute")
async def create_user(request: Request, token: str, db: Session = Depends(get_db)):
    """
    Confirm a user's email.

    This endpoint confirms a user's email address.

    Args:
        request (Request): The request.
        token (str): The confirmation token.
        db (Session): The database session.

    Returns:
        ConfirmResponse: The confirmation response.
    """
    email = await get_email_from_token(token)
    user_controller = UserController(db)
    user = await user_controller.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "You have already confirmed your email"}
    await user_controller.confirm_email(email)
    return {"message": "You have successfully confirmed your email"}