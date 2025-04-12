import pytest
from app.main import app

@pytest.mark.asyncio
async def test_get_current_user(client, auth_headers):
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json() 

@pytest.mark.asyncio
async def test_update_user_avatar(client, auth_headers):
    with open("tests/img/image.png", "rb") as avatar_file:
        files = {"file": avatar_file}
        response = client.patch("/api/users/avatar", files=files, headers=auth_headers)
        assert response.status_code == 200
        assert "avatar" in response.json()