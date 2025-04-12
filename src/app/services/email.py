from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from app.services.auth import create_email_token
from app.config.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Send an email to the user to confirm their email address.

    Args:
        email (EmailStr): The email address of the user.
        username (str): The username of the user.
        host (str): The host URL.

    Raises:
        ConnectionErrors: If there is an error connecting to the email server.
    """
    try:
        """
        Create a token for email verification.
        """
        token_verification = create_email_token({"sub": email})

        """
        Create a message schema for the email.
        """
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        """
        Create a FastMail instance with the connection configuration.
        """
        fm = FastMail(conf)

        """
        Send the email using the FastMail instance.
        """
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        """
        Print any connection errors that occur.
        """
        print(err)