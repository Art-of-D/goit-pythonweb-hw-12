import pytest
from fastapi.testclient import TestClient
from conftest import test_user
from app.main import app
from app.response.schemas import UserCreate
from app.services.auth import create_access_token

@pytest.mark.asyncio
async def test_login_user(client):
    response = client.post("/api/auth/login", data={"username": test_user["name"], "password": test_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = client.post("/api/auth/login", data={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401

new_user = {
    "name": "newuser",
    "email": "newuser@example.com",
    "password": "newpass"
}

@pytest.mark.asyncio
async def test_register_user(client):
    
    response = client.post("/api/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["email"] == new_user["email"]

    response = client.post("/api/auth/register", json=new_user)
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_confirm_email(client):

    valid_token = await create_access_token(data={"id": 1, "sub": new_user["email"], "name": new_user["name"]})

    response = client.get(f"/api/auth/confirm_email/{valid_token}")
    assert response.status_code == 201
    assert response.json()["message"] == "You have successfully confirmed your email"

    response = client.get(f"/api/auth/confirm_email/{valid_token}")
    assert response.status_code == 201
    assert response.json()["message"] == "You have already confirmed your email"

    invalid_token = "invalid_token"
    response = client.get(f"/api/auth/confirm_email/{invalid_token}")
    assert response.status_code == 422
    assert response.json()["detail"] == "Invalid token"