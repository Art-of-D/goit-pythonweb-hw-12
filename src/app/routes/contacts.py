from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.response.schemas import ContactBase, ContactCreate, ContactResponse, ContactListResponse
from app.controllers.contacts import ContactsController
from app.services.current_user import get_current_user
from app.response.schemas import User


router = APIRouter(prefix="/contacts", tags=["contacts"])
"""
API router for contact endpoints.
"""


@router.get("/", response_model=ContactListResponse)
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a list of contacts.

    This endpoint returns a list of contacts for the current user.

    Args:
        skip (int): The number of contacts to skip.
        limit (int): The maximum number of contacts to return.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        ContactListResponse: The list of contacts.
    """
    contacts = ContactsController(db)
    return await contacts.get_contacts(current_user.id, skip, limit)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a contact by ID.

    This endpoint returns a contact by ID for the current user.

    Args:
        contact_id (int): The ID of the contact.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        ContactBase: The contact.
    """
    contact_controller = ContactsController(db)
    contact = await contact_controller.get_by_id(user_id=current_user.id, id=contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new contact.

    This endpoint creates a new contact for the current user.

    Args:
        body (ContactBase): The contact data.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        ContactCreate: The created contact.
    """
    conctact_controller = ContactsController(db)
    try:
        new_contact = ContactCreate(
            user_id=current_user.id, **body.model_dump(exclude_unset=True)
        )
        resp = await conctact_controller.create_contact(new_contact)
        return resp
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_note(
    body: ContactBase,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a contact.

    This endpoint updates a contact by ID for the current user.

    Args:
        body (ContactBase): The updated contact data.
        contact_id (int): The ID of the contact.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        ContactBase: The updated contact.
    """
    contact_controller = ContactsController(db)
    contact = await contact_controller.update_contact(
        user_id=current_user.id, id=contact_id, contact=body
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_conctact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a contact.

    This endpoint deletes a contact by ID for the current user.

    Args:
        contact_id (int): The ID of the contact.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        ContactBase: The deleted contact.
    """
    contact_controller = ContactsController(db)
    contact = await contact_controller.delete_contact(
        user_id=current_user.id, id=contact_id
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact

@router.get("/search", response_model=ContactListResponse)
async def search_contacts(
    name: str = None,
    surname: str = None,
    email: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search for contacts.

    This endpoint searches for contacts by name, surname, or email.

    Args:
        name (str): The name to search for.
        surname (str): The surname to search for.
        email (str): The email to search for.
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        List[ContactBase]: The list of matching contacts.
    """
    contact_controller = ContactsController(db)
    contact = await contact_controller.search_contact(
        user_id=current_user.id, name=name, surname=surname, email=email
    )
    return contact


@router.get("/upcoming-birthdays", response_model=ContactListResponse)
async def upcoming_birthdays(
    db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get upcoming birthdays.

    This endpoint returns a list of contacts with upcoming birthdays.

    Args:
        db (AsyncSession): The database session.
        current_user (User): The current user.

    Returns:
        List[ContactBase]: The list of contacts with upcoming birthdays.
    """
    contact_controller = ContactsController(db)
    birthdays = await contact_controller.get_upcoming_birthdays(user_id=current_user.id)
    return birthdays