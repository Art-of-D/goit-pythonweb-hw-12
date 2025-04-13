import pytest
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import HTTPException
from app.services.auth import Hash, create_access_token, create_email_token, get_email_from_token
from app.config.config import settings

def test_password_hashing():
    hash_util = Hash()
    password = "mysecretpassword"
    hashed_password = hash_util.get_password_hash(password)


    assert hash_util.verify_password(password, hashed_password) is True
    assert hash_util.verify_password("wrongpassword", hashed_password) is False

@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "testuser@example.com"}
    token = await create_access_token(data, expires_delta=60)

    decoded_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert decoded_data["sub"] == "testuser@example.com"
    assert "exp" in decoded_data

@pytest.mark.asyncio
async def test_create_email_token():
    data = {"sub": "testuser@example.com"}
    token = create_email_token(data)

    decoded_data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert decoded_data["sub"] == "testuser@example.com"
    assert "exp" in decoded_data

@pytest.mark.asyncio
async def test_get_email_from_token():
    data = {"sub": "testuser@example.com"}
    token = await create_access_token(data)

    email = await get_email_from_token(token)
    assert email == "testuser@example.com"

    with pytest.raises(HTTPException) as excinfo:
        await get_email_from_token("invalidtoken")
    assert excinfo.value.status_code == 422
    assert excinfo.value.detail == "Invalid token"