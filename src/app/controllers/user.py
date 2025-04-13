from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService
from app.response.schemas import UserCreate, User, UserUpdate


class UserController:
    """
    Controller for managing users.

    Args:
        db (AsyncSession): The database session.
    """

    def __init__(self, db: AsyncSession):
        self.db = UserService(db)

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Get a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user if found.
        """
        user = await self.db.get_user_by_id(user_id)
        return user

    async def get_user_by_username(self, username: str) -> User:
        """
        Get a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user if found.
        """
        user = await self.db.get_user_by_username(username)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """
        Get a user by email.

        Args:
            email (str): The email of the user.

        Returns:
            User: The user if found.
        """
        user = await self.db.get_user_by_email(email)
        return user

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user.

        Args:
            body (UserCreate): The user data.
            avatar (str, optional): The user's avatar. Defaults to None.

        Returns:
            User: The created user.
        """
        user = await self.db.create_user(body, avatar)
        return user

    async def update_user(self, user_id: int, body: UserUpdate) -> User:
        """
        Update a user.

        Args:
            user_id (int): The ID of the user.
            body (User): The updated user data.

        Returns:
            User: The updated user.
        """
        user = await self.db.update_user(user_id, body)
        return user

    async def delete_user(self, user_id: int) -> User:
        """
        Delete a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The deleted user.
        """
        user = await self.db.delete_user(user_id)
        return user

    async def confirm_email(self, email: str) -> None:
        """
        Confirm a user's email.

        Args:
            email (str): The email to confirm.

        Returns:
            None
        """
        return await self.db.confirm_email(email)
    
    async def reset_password(self, email: str) -> None:
        """
        Reset a user's password.

        Args:
            email (str): The email of the user.

        Returns:
            None
        """
        return await self.db.reset_password(email)