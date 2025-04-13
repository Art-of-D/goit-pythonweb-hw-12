import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.contacts import ContactsService
from app.database.models import Contact
from app.response.schemas import ContactCreate, ContactUpdate

@pytest.mark.asyncio
async def test_create_contact(contacts_service, mock_db_session):
    contact_data = ContactCreate(
        name="John", surname="Doe", email="john.doe@example.com",
        phone="1234567890", birthdate="1990-01-01", notes="Friend", user_id=1
    )
    mock_contact = Contact(id=1, **contact_data.model_dump())
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.return_value = mock_contact

    contact = await contacts_service.create_contact(contact_data)

    assert contact.name == "John"
    assert contact.email == "john.doe@example.com"
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_get_contacts():
    mock_contacts = [
        Contact(id=1, name="John", surname="Doe", email="john.doe@example.com", user_id=1),
        Contact(id=2, name="Jane", surname="Doe", email="jane.doe@example.com", user_id=1)
    ]

    mock_db_session = AsyncMock(spec=AsyncSession)
    contacts_service = ContactsService(mock_db_session)

    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_contacts
    mock_result.scalars.return_value = mock_scalars
    mock_db_session.execute.return_value = mock_result 

    contacts = await contacts_service.get_contacts(user_id=1)

    assert len(contacts) == 2
    assert contacts[0].name == "John"
    mock_db_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact(contacts_service, mock_db_session):
    mock_contact = Contact(id=1, name="John", surname="Doe", email="john.doe@example.com", user_id=1)
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_contact
    mock_result.scalars.return_value = mock_scalars
    mock_db_session.execute.return_value = mock_result

    updated_data = ContactUpdate(name="Johnny", email="johnny.doe@example.com")
    contact = await contacts_service.update_contact(user_id=1, id=1, contact=updated_data)

    assert contact.name == "Johnny"
    assert contact.email == "johnny.doe@example.com"
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_delete_contact(contacts_service, mock_db_session):
    mock_contact = Contact(id=1, name="John", surname="Doe", email="john.doe@example.com", user_id=1)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_contact
    mock_db_session.execute.return_value = mock_result
    contact = await contacts_service.delete_contact(user_id=1, id=1)

    assert contact.id == 1
    mock_db_session.delete.assert_called_once_with(mock_contact)
    mock_db_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_search_contacts(contacts_service, mock_db_session):
    mock_contacts = [
        Contact(id=1, name="John", surname="Doe", email="john.doe@example.com", user_id=1)
    ]
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_contacts
    mock_result.scalars.return_value = mock_scalars
    mock_db_session.execute.return_value = mock_result

    contacts = await contacts_service.search_contacts(user_id=1, name="John")

    assert len(contacts) == 1
    assert contacts[0].name == "John"
    mock_db_session.execute.assert_called_once()

@pytest.mark.asyncio
async def test_get_upcoming_birthdays(contacts_service, mock_db_session):
    mock_contacts = [
        Contact(id=1, name="John", surname="Doe", email="john.doe@example.com", birthdate="1990-01-01", user_id=1)
    ]
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = mock_contacts
    mock_result.scalars.return_value = mock_scalars
    mock_db_session.execute.return_value = mock_result

    contacts = await contacts_service.get_upcoming_birthdays(user_id=1)

    assert len(contacts) == 1
    assert contacts[0].name == "John"
    mock_db_session.execute.assert_called_once()