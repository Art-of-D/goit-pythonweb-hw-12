
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, User
from app.services.auth import Hash
from app.main import app
from fastapi.testclient import TestClient
from app.database.db import get_db
from app.services.auth import create_access_token

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
        )
        session.add(current_user)
        await session.commit()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="module")
def client():

    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest_asyncio.fixture(scope="module")
async def auth_headers():
    token = await create_access_token(data={"id": 0, "sub": test_user["email"], "name": test_user["name"]})
    return {"Authorization": f"Bearer {token}"}