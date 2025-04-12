import pytest
from datetime import datetime
from app.response.schemas import ContactResponse

class DummyContact:
    def __init__(self):
        self.id = 1
        self.name = "John"
        self.surname = "Smith"
        self.email = "john@example.com"
        self.phone = "1234567890"
        self.birthdate = datetime(2000, 1, 1)
        self.notes = "My friend"
        self.user_id = 0

def test_contactbase_from_orm():
    """
    Tests ContactResponse.from_orm() method.

    The method should properly create an instance of ContactBase from a given ORM object.

    The test creates a DummyContact object and checks that its fields are properly copied to an instance of ContactResponse.
    """
    dummy = DummyContact()
    contact = ContactResponse.from_orm(dummy)

    assert contact.name == "John"
    assert contact.birthdate == "2000-01-01"

def test_contactcreate_from_orm():
    dummy = DummyContact()
    contact = ContactResponse.from_orm(dummy)

    assert contact.user_id == 0
    assert contact.birthdate == "2000-01-01"