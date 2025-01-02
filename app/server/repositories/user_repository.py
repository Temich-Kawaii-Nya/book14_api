from abc import ABC, abstractmethod

from beanie import PydanticObjectId

from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError

class IUserRepository(ABC):
    """
    Interface for managing user data.
    """

    @abstractmethod
    async def add_user(self, user: User) -> RepositoryError | None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: PydanticObjectId) -> RepositoryError | None:
        pass

    @abstractmethod
    async def update_user(self, user_id: PydanticObjectId, updated_data: dict) -> RepositoryError | None:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: PydanticObjectId) -> RepositoryError | User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> RepositoryError | User:
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

    async def get_user_by_email(self, email: str) -> RepositoryError | User:
        return await User.find_one(User.email == email)