from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis
import json

from app.database.db import get_db
from app.services.user import UserService
from app.config.config import settings
from app.response.schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
redis_client = aioredis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """
    Get the current user from the token.

    Args:
        token (str): The token to validate.
        db (AsyncSession): The database session.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cached_user = await redis_client.get(f"user:{token}")
    if cached_user:
        print("!!!!!!!!!!!!!!!!!!!")
        print(cached_user)
        print("!!!!!!!!!!!!!!!!!!!")
        return User(**json.loads(cached_user))
    try:
        """
        Decode the token and extract the username.
        """
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("name")
        if username is None:
            raise credentials_exception
    except JWTError:
        """
        Raise an exception if the token is invalid.
        """
        raise credentials_exception

    """
    Get the user service instance.
    """
    user_service = UserService(db)

    """
    Get the user by username.
    """

    user = await user_service.get_user_by_username(username)
    if user is None:
        """
        Raise an exception if the user is not found.
        """
        raise credentials_exception
        
    user_data = {
    "id": user.id,
    "name": user.name,
    "email": user.email,
    "avatar": user.avatar,
    "role": user.role
    }
    
    await redis_client.setex(f"user:{token}", 3600, json.dumps(user_data))
    return user