from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional
import jwt
from beanie import PydanticObjectId
from jwt import InvalidTokenError, PyJWTError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.server.config import config
from app.server.models.user import User, SignupData, LoginData
from app.server.repositories.repository_error import RepositoryError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class IUserRepository(ABC):
    """
    Interface for managing user data.
    """

    @abstractmethod
    async def add_user(self, user: User) -> RepositoryError | None:
        """
        Add a new user to the database.

        :param user: The user object to add.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: PydanticObjectId) -> RepositoryError | None:
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def update_user(self, user_id: PydanticObjectId, updated_data: dict) -> RepositoryError | None:
        """
        Update user data.

        :param user_id: The ID of the user to update.
        :param updated_data: A dictionary of the updated user data.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: PydanticObjectId) -> RepositoryError | User:
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> RepositoryError | User:
        """
        Retrieve a user by their email.

        :param email: The email of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        pass

class UserRepository(IUserRepository, ABC):
    """
    Repository for managing user data.
    """

    async def add_user(self, user: User) -> RepositoryError | None:
        existing_user = await User.find_one(User.email == user.email)
        if existing_user:
            return RepositoryError(message=f"User with email {user.email} already exists.")
        await user.create()
        return None

    async def delete_user(self, user_id: PydanticObjectId) -> RepositoryError | None:
        user = await User.get(user_id)
        if not user:
            return RepositoryError(message=f"User with ID {user_id} not found.")
        await user.delete()
        return None

    async def update_user(self, user_id: PydanticObjectId, updated_data: dict) -> RepositoryError | None:
        user = await User.get(user_id)
        if not user:
            return RepositoryError(message=f"User with ID {user_id} not found.")
        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await user.save()
        return None

    async def get_user_by_id(self, user_id: PydanticObjectId) -> RepositoryError | User:
        return await User.get(user_id)

    async def get_user_by_email(self, email: EmailStr) -> RepositoryError | User:
        return await User.find_one(User.email == email)
    async def get_user_by_name(self, username: str) -> RepositoryError | User:
        return await User.find_one(User.username == username)