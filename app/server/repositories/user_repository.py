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
    async def add_user(self, user: User):
        """
        Add a new user to the database.

        :param user: The user object to add.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_user(self, user_id: PydanticObjectId):
        """
        Delete a user by their ID.

        :param user_id: The ID of the user to delete.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def update_user(self, user_id: PydanticObjectId, updated_data: dict):
        """
        Update user data.

        :param user_id: The ID of the user to update.
        :param updated_data: A dictionary of the updated user data.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: PydanticObjectId) -> User:
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieve a user by their email.

        :param email: The email of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_user_by_name(self, username: str) -> User:
        """
        Retrieve a user by their email.

        :param username: The username of the user to retrieve.
        :return: The User object if found, otherwise None.
        """
        pass

class UserRepository(IUserRepository, ABC):
    """
    Repository for managing user data.
    """

    async def add_user(self, user: User) -> PydanticObjectId:
        existing_user = await User.find_one(User.email == user.email)
        if existing_user:
            raise RepositoryError(message=f"User with email {user.email} already exists.", statuscode=400)
        await user.create()
        return user.id

    async def delete_user(self, user_id: PydanticObjectId) -> PydanticObjectId:
        user = await User.get(user_id)
        if not user:
            raise RepositoryError(message=f"User with ID {user_id} not found.", statuscode=404)
        await user.delete()
        return user.id

    async def update_user(self, user_id: PydanticObjectId, updated_data: dict):
        user = await User.get(user_id)
        if not user:
            raise RepositoryError(message=f"User with ID {user_id} not found.", statuscode=404)
        for key, value in updated_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        await user.save()

    async def get_user_by_id(self, user_id: PydanticObjectId) -> RepositoryError | User:
        return await User.get(user_id)

    async def get_user_by_email(self, email: EmailStr) -> RepositoryError | User:
        return await User.find_one(User.email == email)
    async def get_user_by_name(self, username: str) -> RepositoryError | User:
        return await User.find_one(User.username == username)