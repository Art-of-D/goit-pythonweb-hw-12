from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from typing import Optional
from enum import Enum

Base = declarative_base()

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    """
    User model.

    This class represents a user in the database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    """
    User ID.

    The unique identifier for the user.
    """

    name = Column(String, nullable=False)
    """
    User name.

    The name of the user.
    """

    email = Column(String, nullable=False)
    """
    User email.

    The email address of the user.
    """

    password = Column(String, nullable=False)
    """
    User password.

    The password of the user.
    """

    avatar = Column(String, nullable=True)
    """
    User avatar.

    The avatar of the user.
    """

    confirmed = Column(Boolean, default=False)
    """
    User confirmation.

    Whether the user has confirmed their email address.
    """

    contacts = relationship("Contact", back_populates="user", cascade="all, delete")
    """
    User contacts.

    The contacts associated with the user.
    """
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    """
    User role.

    The role of the user in the system.
    """

class Contact(Base):
    """
    Contact model.

    This class represents a contact in the database.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    """
    Contact ID.

    The unique identifier for the contact.
    """

    name = Column(String, nullable=False)
    """
    Contact name.

    The name of the contact.
    """

    surname = Column(String, nullable=False)
    """
    Contact surname.

    The surname of the contact.
    """

    email = Column(String, nullable=False)
    """
    Contact email.

    The email address of the contact.
    """

    phone = Column(String, nullable=False)
    """
    Contact phone.

    The phone number of the contact.
    """

    birthdate = Column(Date, nullable=False)
    """
    Contact birthdate.

    The birthdate of the contact.
    """

    notes: Optional[str] = Column(String, nullable=True)
    """
    Contact notes.

    Any additional notes about the contact.
    """

    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    """
    User ID.

    The ID of the user who owns the contact.
    """

    user = relationship("User", back_populates="contacts")
    """
    User.

    The user who owns the contact.
    """