import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from jose import jwt
from unittest.mock import MagicMock, AsyncMock
import redis.asyncio as aioredis

from app.config.config import settings
from app.database.models import Base, User
from app.database.db import get_db
from app.services.auth import Hash
from app.services.user import UserService
from app.services.contacts import ContactsService
from app.services.auth import create_access_token
from app.main import app

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

test_user = {
    "name": "testuser",
    "email": "testuser@example.com",
    "password": "testpass",
    "avatar": "https://www.avatar.com/pandorapedia/jake-sully",
    "role": "ADMIN"
}

@pytest_asyncio.fixture(scope="module", autouse=True)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        hash_password = Hash().get_password_hash(test_user["password"])
        current_user = User(
            name=test_user["name"],
            email=test_user["email"],
            password=hash_password,
            confirmed=True,
            avatar=test_user["avatar"],
            role=test_user["role"]
        )
        session.add(current_user)
        await session.commit()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()

@pytest_asyncio.fixture
async def auth_headers():
    token = await create_access_token(data={"id": 0, "sub": test_user["email"], "name": test_user["name"]})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def token():
    def _generate_token(name="testuser"):
        payload = {"name": name}
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return _generate_token

@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=AsyncSession)
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.add = MagicMock()
    return session

@pytest.fixture
def user_service(mock_db_session):
    return UserService(session=mock_db_session)

@pytest.fixture
def contacts_service(mock_db_session):
    return ContactsService(session=mock_db_session)

@pytest_asyncio.fixture
async def mock_user_service(mocker):
    mock_user = User(
        name="testuser",
        email="testuser@example.com",
        avatar="https://www.avatar.com/pandorapedia/jake-sully",
        role="ADMIN",
        id=1
    )
    mock_service_class = mocker.patch("app.services.user.UserService")
    mock_service_instance = mock_service_class.return_value
    mock_service_instance.get_user_by_username = AsyncMock(return_value=mock_user)
    return mock_service_instance