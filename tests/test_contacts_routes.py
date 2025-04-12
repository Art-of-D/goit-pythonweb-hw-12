import pytest
from app.main import app
from conftest import test_user


@pytest.mark.asyncio
async def test_create_contact(client, auth_headers):
    contact_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01"
    }
    response = client.post("/api/contacts/", json=contact_data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["email"] == contact_data["email"]

@pytest.mark.asyncio
async def test_read_contacts(client, auth_headers):
    response = client.get("/api/contacts/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json()["contacts"], list)

@pytest.mark.asyncio
async def test_update_contact(client, auth_headers):
    contact_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01"
    }
    create_response = client.post("/api/contacts/", json=contact_data, headers=auth_headers)
    assert create_response.status_code == 201
    contact_id = create_response.json()["id"]

    contact_data = {
        "name": "Jane",
        "surname": "Doe",
        "email": "jane.doe@example.com",
        "phone": "0987654321",
        "birthdate": "1992-02-02"
    }
    response = client.put(f"/api/contacts/{contact_id}", json=contact_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == contact_data["email"]

@pytest.mark.asyncio
async def test_delete_contact(client, auth_headers):
    contact_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthdate": "1990-01-01"
    }
    create_response = client.post("/api/contacts/", json=contact_data, headers=auth_headers)
    assert create_response.status_code == 201
    contact_id = create_response.json()["id"]

    response = client.delete(f"/api/contacts/{contact_id}", headers=auth_headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_search_contacts(client, auth_headers):
    response = client.get("/api/contacts/search?surname=Doe", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json()["contacts"], list)

@pytest.mark.asyncio
async def test_upcoming_birthdays(client, auth_headers):
    response = client.get("/api/contacts/upcoming-birthdays", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json()["contacts"], list)