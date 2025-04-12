from sqlalchemy.ext.asyncio import AsyncSession

from app.services.contacts import ContactsService
from app.response.schemas import ContactBase, ContactCreate, ContactResponse


class ContactsController:
    """
    Controller for managing contacts.

    Args:
        db (AsyncSession): The database session.
    """

    def __init__(self, db: AsyncSession):
        self.db = ContactsService(db)

    async def create_contact(self, contact: ContactCreate) -> ContactResponse:
        """
        Create a new contact.

        Args:
            contact (ContactCreate): The contact to create.

        Returns:
            ContactCreate: The created contact.
        """
        created_contact = await self.db.create_contact(contact)
        return ContactResponse.from_orm(created_contact)

    async def get_contacts(self, user_id: int, skip: int = 0, limit: int = 10) -> dict:
        """
        Get a list of contacts for a user.

        Args:
            user_id (int): The ID of the user.
            skip (int, optional): The number of contacts to skip. Defaults to 0.
            limit (int, optional): The maximum number of contacts to return. Defaults to 10.

        Returns:
            dict: A dictionary containing the list of contacts.
        """
        contacts = await self.db.get_contacts(user_id, skip, limit)
        return {"contacts": [ContactResponse.from_orm(contact) for contact in contacts]}

    async def get_by_id(self, user_id: int, id: int) -> ContactResponse | None:
        """
        Get a contact by ID.

        Args:
            user_id (int): The ID of the user.
            id (int): The ID of the contact.

        Returns:
            ContactBase | None: The contact if found, otherwise None.
        """
        contact = await self.db.get_by_id(user_id, id)
        if contact is None:
            return None
        return ContactResponse.from_orm(contact)

    async def update_contact(self, user_id: int, id: int, contact: ContactBase) -> ContactResponse:
        """
        Update a contact.

        Args:
            user_id (int): The ID of the user.
            id (int): The ID of the contact.
            contact (ContactBase): The updated contact.

        Returns:
            ContactResponse: The updated contact.
        """
        updated_contact = await self.db.update_contact(user_id, id, contact)
        return ContactResponse.from_orm(updated_contact)

    async def delete_contact(self, user_id: int, id: int) -> ContactBase:
        """
        Delete a contact.

        Args:
            user_id (int): The ID of the user.
            id (int): The ID of the contact.

        Returns:
            ContactBase: The deleted contact.
        """
        deleted_contact = await self.db.delete_contact(user_id, id)
        return ContactResponse.from_orm(deleted_contact)

    async def search_contact(
        self, user_id: int, name: str = None, surname: str = None, email: str = None
    ) -> dict:
        """
        Search for contacts.

        Args:
            user_id (int): The ID of the user.
            name (str, optional): The name to search for. Defaults to None.
            surname (str, optional): The surname to search for. Defaults to None.
            email (str, optional): The email to search for. Defaults to None.

        Returns:
            dict: A dictionary containing the list of matching contacts.
        """
        contacts = await self.db.search_contacts(user_id, name, surname, email)
        return {"contacts": [ContactResponse.from_orm(contact) for contact in contacts]}

    async def get_upcoming_birthdays(self, user_id: int) -> dict:
        """
        Get a list of contacts with upcoming birthdays.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: A dictionary containing the list of contacts with upcoming birthdays.
        """
        contacts = await self.db.get_upcoming_birthdays(user_id)
        return {"contacts": [ContactResponse.from_orm(contact) for contact in contacts]}