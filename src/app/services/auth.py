from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from typing import Optional
from app.config.config import settings

class Hash:
    """
    Password hashing utility class.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password (str): The plain password.
            hashed_password (str): The hashed password.

        Returns:
            bool: Whether the passwords match.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Get a hashed password from a plain password.

        Args:
            password (str): The plain password.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)


async def create_access_token(data: dict, expires_delta: Optional[float] = None):
    """
    Create an access token.

    Args:
        data (dict): The token data.
        expires_delta (Optional[float]): The token expiration time in seconds.

    Returns:
        str: The access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_email_token(data: dict):
    """
    Create an email token.

    Args:
        data (dict): The token data.

    Returns:
        str: The email token.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_email_from_token(token: str):
    """
    Get the email from a token.

    Args:
        token (str): The token.

    Returns:
        str: The email.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload["sub"]
        return email
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid token",
        )