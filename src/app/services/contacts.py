from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, and_
from datetime import datetime, timedelta, timezone

from app.database.models import Contact
from app.response.schemas import ContactBase, ContactCreate, ContactUpdate


class ContactsService:
    """
    Service class for managing contacts.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the service with a database session.

        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def create_contact(self, contact: ContactCreate):
        """
        Create a new contact.

        Args:
            contact (ContactCreate): The contact data.

        Returns:
            Contact: The created contact.

        Raises:
            ValueError: If the contact data is invalid.
            RuntimeError: If an error occurs during creation.
        """
        if contact is None:
            raise ValueError("Contact cannot be None.")
        new_contact = Contact(
            name=contact.name,
            surname=contact.surname,
            email=contact.email,
            phone=contact.phone,
            birthdate=self.str_to_date(contact.birthdate),
            notes=contact.notes,
            user_id=contact.user_id,
        )
        try:
            self.session.add(new_contact)
            await self.session.commit()
            await self.session.refresh(new_contact)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"An error occurred while creating the contact: {e}")
        return new_contact

    async def get_contacts(self, user_id: int, skip: int = 0, limit: int = 10):
        """
        Get a list of contacts for a user.

        Args:
            user_id (int): The user ID.
            skip (int): The number of contacts to skip.
            limit (int): The maximum number of contacts to return.

        Returns:
            List[Contact]: The list of contacts.

        Raises:
            ValueError: If no contacts are found.
        """
        stmt = (
            select(Contact).where(Contact.user_id == user_id).offset(skip).limit(limit)
        )
        result = await self.session.execute(stmt)
        if result is None:
            raise ValueError("No contacts found.")
        return result.scalars().all()

    async def get_by_id(self, user_id: int, id: int):
        """
        Get a contact by ID.

        Args:
            user_id (int): The user ID.
            id (int): The contact ID.

        Returns:
            Contact: The contact.

        Raises:
            ValueError: If the contact is not found.
        """
        stmt = select(Contact).where(user_id == Contact.user_id, Contact.id == id)
        result = await self.session.execute(stmt)
        contact = result.scalar_one_or_none()
        if result is None:
            raise ValueError(f"Contact with the given ID {id} does not exist.")
        return contact

    async def update_contact(self, user_id: int, id: int, contact: ContactUpdate):
        """
        Update a contact.

        Args:
            user_id (int): The user ID.
            id (int): The contact ID.
            contact (ContactUpdate): The updated contact data.

        Returns:
            Contact: The updated contact.

        Raises:
            ValueError: If the contact is not found.
            RuntimeError: If an error occurs during update.
        """
        existing_contact = await self.get_by_id(user_id, id)
        if existing_contact is None:
            raise ValueError("Contact with the given ID does not exist.")

        if contact.name:
            existing_contact.name = contact.name
        if contact.surname:
            existing_contact.surname = contact.surname
        if contact.email:
            existing_contact.email = contact.email
        if contact.phone:
            existing_contact.phone = contact.phone
        if contact.birthdate:
            existing_contact.birthdate = self.str_to_date(contact.birthdate)
        if contact.notes:
            existing_contact.notes = contact.notes
        try:
            self.session.add(existing_contact)
            await self.session.commit()
            await self.session.refresh(existing_contact)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Failed to update contact: {e}")

        return existing_contact
    
    async def delete_contact(self, user_id: int, id: int):
        """
        Delete a contact.

        Args:
            user_id (int): The user ID.
            id (int): The contact ID.

        Returns:
            Contact: The deleted contact.

        Raises:
            ValueError: If the contact is not found.
            RuntimeError: If an error occurs during deletion.
        """
        try:
            contact = await self.get_by_id(user_id, id)
            if contact is None:
                raise ValueError(f"Contact with the given ID {id} does not exist.")
            await self.session.delete(contact)
            await self.session.commit()
            return contact
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Failed to delete contact. {e}")

    async def search_contacts(
        self, user_id: int, name: str = None, surname: str = None, email: str = None
    ):
        """
        Search for contacts.

        Args:
            user_id (int): The user ID.
            name (str): The name to search for.
            surname (str): The surname to search for.
            email (str): The email to search for.

        Returns:
            List[Contact]: The list of matching contacts.
        """
        stmt = select(Contact).where(user_id == Contact.user_id)

        if name:
            stmt = stmt.filter(Contact.name.ilike(f"%{name}%"))
        if surname:
            stmt = stmt.filter(Contact.surname.ilike(f"%{surname}%"))
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_upcoming_birthdays(self, user_id: int):
        """
        Get upcoming birthdays.

        Args:
            user_id (int): The user ID.

        Returns:
            List[Contact]: The list of contacts with upcoming birthdays.
        """
        today = datetime.now(timezone.utc).date()
        next_week = today + timedelta(days=7)

        query = (
            select(Contact)
            .where(user_id == Contact.user_id)
            .filter(
                and_(
                    extract("month", Contact.birthdate) == today.month,
                    extract("day", Contact.birthdate) >= today.day,
                    extract("day", Contact.birthdate) < next_week.day,
                )
                | and_(
                    extract("month", Contact.birthdate) == next_week.month,
                    extract("day", Contact.birthdate) < next_week.day,
                )
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    @staticmethod
    def str_to_date(date_str):
        """
        Convert a date string to a date object.

        Args:
            date_str (str): The date string.

        Returns:
            date: The date object.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None