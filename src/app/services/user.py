from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.response.schemas import UserCreate
from sqlalchemy import select


class UserService:
    """
    Service class for user-related operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the service with a database session.

        Args:
            session (AsyncSession): The database session.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Get a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User | None: The user if found, otherwise None.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Get a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user if found, otherwise None.
        """
        stmt = select(User).filter_by(name=username)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Get a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The user if found, otherwise None.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user.

        Args:
            body (UserCreate): The user data.
            avatar (str, optional): The user's avatar. Defaults to None.

        Returns:
            User: The created user.
        """
        user = User(**body.model_dump(exclude_unset=True), avatar=avatar)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        """
        Delete a user by their ID.

        Args:
            user_id (int): The ID of the user.
        """
        await self.db.delete(User, user_id)
        await self.db.commit()
        return

    async def confirm_email(self, email: str):
        """
        Confirm a user's email.

        Args:
            email (str): The email of the user.
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_user(self, user_id: int, body: User) -> User:
        """
        Update a user's data.

        Args:
            user_id (int): The ID of the user.
            body (User): The updated user data.

        Returns:
            User: The updated user.
        """
        user = await self.get_user_by_id(user_id)
        if body.name:
            user.name = body.name
        if body.email:
            user.email = body.email 
        if body.password:
            user.password = body.password
        if body.avatar:
            user.avatar = body.avatar
        await self.db.commit()
        await self.db.refresh(user)
        return user