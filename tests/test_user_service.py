import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.response.schemas import UserCreate, UserUpdate

mock_user = User(
    id=1,
    name="testuser",
    email="testuser@example.com",
    password="hashedpassword",
    confirmed=True,
)

@pytest.mark.asyncio
async def test_get_user_by_id(user_service, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = mock_user
    mock_db_session.execute.return_value = mock_result

    user = await user_service.get_user_by_id(mock_user.id)


    assert user.id == mock_user.id
    assert user.name == mock_user.name
    assert user.email == mock_user.email
    mock_db_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_create_user(user_service, mock_db_session):
    user_data = UserCreate(name="newuser", email="newuser@example.com", password="password")

    async def mock_refresh(instance):
        instance.id = 2

    mock_db_session.refresh.side_effect = mock_refresh

    user = await user_service.create_user(user_data)

    assert user.name == "newuser"
    assert user.email == "newuser@example.com"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_delete_user(user_service, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = mock_user
    mock_db_session.execute.return_value = mock_result

    await user_service.delete_user(mock_user.id)

    mock_db_session.delete.assert_called_once_with(mock_user)
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_confirm_email(user_service, mock_db_session):
    mock_user.confirmed = False
    mock_result = MagicMock()
    mock_result.scalar.return_value = mock_user
    mock_db_session.execute.return_value = mock_result

    await user_service.confirm_email("testuser@example.com")

    assert mock_user.confirmed is True
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_update_user(user_service, mock_db_session):
    mock_result = MagicMock()
    mock_result.scalar.return_value = mock_user
    mock_db_session.execute.return_value = mock_result

    updated_user = UserUpdate(
        name = "newname",
        email = "newemail@example.com",
        password = "newpassword",
        avatar = "newavatar")

    async def mock_refresh(instance):
        pass

    mock_db_session.refresh.side_effect = mock_refresh

    user = await user_service.update_user(1, updated_user)

    assert user.name == updated_user.name
    assert user.email == updated_user.email
    assert user.password == updated_user.password
    assert user.avatar == updated_user.avatar
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()