import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from app.config.config import settings as config


class DatabaseSessionManager:
    """
    Manager for database sessions.

    This class creates and manages database sessions using SQLAlchemy.
    """

    def __init__(self, url: str):
        """
        Initialize the database session manager.

        Args:
            url (str): The URL of the database to connect to.
        """
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """
        Get a database session.

        This method yields a database session that can be used to execute queries.
        If an error occurs, the session is rolled back and the error is re-raised.

        Yields:
            AsyncSession: The database session.
        """
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """
    Get a database session.

    This function yields a database session that can be used to execute queries.

    Yields:
        AsyncSession: The database session.
    """
    async with sessionmanager.session() as session:
        yield session