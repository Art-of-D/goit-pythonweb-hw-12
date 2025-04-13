import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch, MagicMock
import json

from app.main import app
from app.services.current_user import get_current_user
from app.response.schemas import User

@pytest.mark.asyncio
async def test_get_current_user_valid_token(mock_db_session, token):
    fake_user = MagicMock()
    fake_user.id = 123
    fake_user.name = "testuser"
    fake_user.email = "test@example.com"
    fake_user.avatar = "http://example.com/avatar.png"
    fake_user.role = "user"

    with patch("app.services.current_user.redis_client.get", new_callable=AsyncMock, return_value=None), \
         patch("app.services.current_user.redis_client.setex", new_callable=AsyncMock, return_value=True), \
         patch("app.services.current_user.jwt.decode", return_value={"name": "testuser"}), \
         patch("app.services.current_user.UserService") as MockUserService:

        mock_user_service_instance = MockUserService.return_value
        mock_user_service_instance.get_user_by_username = AsyncMock(return_value=fake_user)

        user = await get_current_user(token(), mock_db_session)

        assert user.id == 123
        assert user.name == "testuser"
        assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_db_session):
    with patch('app.services.current_user.redis_client.get', new_callable=AsyncMock, return_value=None), \
         patch('app.services.current_user.jwt.decode', side_effect=HTTPException(status_code=401)):
        
        with pytest.raises(HTTPException):
            await get_current_user("invalid_token", mock_db_session)



@pytest.mark.asyncio
async def test_get_current_user_user_not_found(mock_db_session, token):
    valid_token = token(name="nonexistentuser")

    with patch("app.services.current_user.redis_client.get", new_callable=AsyncMock, return_value=None), \
         patch("app.services.current_user.jwt.decode", return_value={"name": "nonexistentuser"}), \
         patch("app.services.current_user.UserService") as MockUserService:

        mock_user_service_instance = MockUserService.return_value
        mock_user_service_instance.get_user_by_username = AsyncMock(return_value=None)

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(valid_token, mock_db_session)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"

@pytest.mark.asyncio
async def test_get_current_user_cached_user(mock_db_session, token):
    user_data = {
        "id": 123,
        "name": "testuser",
        "email": "testuser@example.com",
        "avatar": "https://www.avatar.com/pandorapedia/jake-sully",
        "role": "ADMIN",
        "confirmed": True,
    }

    access_token = token(name="testuser")

    with patch("app.services.current_user.redis_client.get", new_callable=AsyncMock, return_value=json.dumps(user_data)):
        user = await get_current_user(access_token, mock_db_session)
        assert user.name == "testuser"
        assert user.email == "testuser@example.com"