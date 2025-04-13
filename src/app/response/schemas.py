from typing import Optional, List
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    """
    Base contact model.

    This class represents a contact with basic information.
    """
    name: str = Field(max_length=50)
    """
    Contact name.

    The name of the contact.
    """

    surname: str = Field(max_length=50)
    """
    Contact surname.

    The surname of the contact.
    """

    email: str = Field(max_length=150)
    """
    Contact email.

    The email address of the contact.
    """

    phone: str = Field(max_length=20)
    """
    Contact phone.

    The phone number of the contact.
    """

    birthdate: str
    """
    Contact birthdate.

    The birthdate of the contact in the format "YYYY-MM-DD".
    """

    notes: Optional[str] = None
    """
    Contact notes.

    Any additional notes about the contact.
    """



class ContactCreate(ContactBase):
    """
    Contact creation model.

    This class represents a contact with basic information and a user ID.
    """
    user_id: int
    """
    User ID.

    The ID of the user who owns the contact.
    """

class ContactUpdate(BaseModel):
    """
    Contact update model.

    This class represents a contact with basic information.
    """
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[str] = None
    notes: Optional[str] = None

class ContactResponse(ContactCreate):
    """
    Contact response model.

    This class represents a contact with additional information.
    """

    id: int
    """
    Contact ID.

    The ID of the contact.
    """
    @classmethod
    def from_orm(cls, obj):
        """
        Create a ContactBase instance from an ORM object.

        Args:
            obj: The ORM object to create the instance from.

        Returns:
            ContactBase: The created instance.
        """
        return cls(
            id=obj.id,
            name=obj.name,
            surname=obj.surname,
            email=obj.email,
            phone=obj.phone,
            birthdate=obj.birthdate.strftime("%Y-%m-%d"),
            notes=obj.notes,
            user_id=obj.user_id
        )
    


class ContactListResponse(BaseModel):
    """
    Contact list response model.

    This class represents a list of contacts.
    """

    contacts: List[ContactResponse]
    """
    Contacts.

    The list of contacts.
    """


class User(BaseModel):
    """
    User model.

    This class represents a user with basic information.
    """

    id: int
    """
    User ID.

    The ID of the user.
    """

    name: str
    """
    User name.

    The name of the user.
    """

    email: str
    """
    User email.

    The email address of the user.
    """

    avatar: Optional[str]
    """
    User avatar.

    The avatar of the user.
    """
    role: str
    """
    User role.

    The role of the user.
    """ 
class UserCreate(BaseModel):
    """
    User creation model.

    This class represents a user with basic information and a password.
    """

    name: str
    """
    User name.

    The name of the user.
    """

    email: str
    """
    User email.

    The email address of the user.
    """

    password: str
    """
    User password.

    The password of the user.
    """

    role: Optional[str] = None
    """
    User role.

    The role of the user.
    """

class UserUpdate(BaseModel):
    """
    User update model.

    This class represents a user with basic information.
    """

    name: Optional[str] = None
    """
    User name.

    The name of the user.
    """

    email: Optional[str] = None
    """
    User email.

    The email address of the user.
    """

    password: Optional[str] = None
    """
    User password.

    The password of the user.
    """

    avatar: Optional[str] = None
    """
    User avatar.

    The avatar of the user.
    """

    role: Optional[str] = None
    """
    User role.

    The role of the user.
    """


class ConfirmResponse(BaseModel):
    """
    Confirmation response model.

    This class represents a confirmation response with a message.
    """

    message: str
    """
    Message.

    The confirmation message.
    """


class Token(BaseModel):
    """
    Token model.

    This class represents a token with an access token and a token type.
    """

    access_token: str
    """
    Access token.

    The access token.
    """

    token_type: str
    """
    Token type.

    The type of the token.
    """