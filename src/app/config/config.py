from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    This class defines the application's settings, including database, JWT, email, and cloud storage settings.
    """

    DB_URL: str
    """
    Database URL.

    The URL of the database to connect to.
    """

    JWT_SECRET: str
    """
    JWT secret key.

    The secret key used to sign and verify JWT tokens.
    """

    JWT_ALGORITHM: str
    """
    JWT algorithm.

    The algorithm used to sign and verify JWT tokens.
    """

    JWT_EXPIRATION_SECONDS: int
    """
    JWT expiration time.

    The time in seconds after which JWT tokens expire.
    """

    MAIL_USERNAME: EmailStr
    """
    Email username.

    The username to use when sending emails.
    """

    MAIL_PASSWORD: str
    """
    Email password.

    The password to use when sending emails.
    """

    MAIL_FROM: EmailStr
    """
    Email from address.

    The email address to use as the "from" address when sending emails.
    """

    MAIL_PORT: int
    """
    Email port.

    The port to use when sending emails.
    """

    MAIL_SERVER: str
    """
    Email server.

    The server to use when sending emails.
    """

    MAIL_FROM_NAME: str
    """
    Email from name.

    The name to use as the "from" name when sending emails.
    """

    MAIL_STARTTLS: bool
    """
    Email start TLS.

    Whether to use STARTTLS when sending emails.
    """

    MAIL_SSL_TLS: bool
    """
    Email SSL/TLS.

    Whether to use SSL/TLS when sending emails.
    """

    USE_CREDENTIALS: bool
    """
    Use credentials.

    Whether to use credentials when sending emails.
    """

    VALIDATE_CERTS: bool
    """
    Validate certificates.

    Whether to validate certificates when sending emails.
    """

    CLD_NAME: str
    """
    Cloud name.

    The name of the cloud storage service to use.
    """

    CLD_API_KEY: str
    """
    Cloud API key.

    The API key to use when accessing the cloud storage service.
    """

    CLD_API_SECRET: str
    """
    Cloud API secret.

    The API secret to use when accessing the cloud storage service.
    """

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )
    """
    Model configuration.

    The configuration for the Pydantic model.
    """
    

settings = Settings()

