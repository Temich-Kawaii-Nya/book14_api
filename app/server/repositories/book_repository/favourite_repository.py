from abc import ABC, abstractmethod
from typing import Optional

from beanie import PydanticObjectId

from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError


class IFavouriteRepository(ABC):
    @abstractmethod
    async def add_to_favourites(self, user_id, book_id: PydanticObjectId):
        pass

    @abstractmethod
    async def remove_from_favourites(self, user_id, book_id: PydanticObjectId):
        pass


async def _validate_user_and_book(
        user_id: PydanticObjectId, book_id: PydanticObjectId
) -> Optional[RepositoryError]:
    user_data = await User.get(user_id)
    if not user_data:
        return RepositoryError(message=f"User with id {user_id} not found")

    if not any(book.id == book_id for book in user_data.userBooks):
        return RepositoryError(message=f"Book with id {book_id} not found in user's book list")

    return None


class FavouriteRepository(IFavouriteRepository, ABC):

    async def add_to_favourites(self, user_id, book_id: PydanticObjectId) -> RepositoryError | None:
        error = await _validate_user_and_book(user_id, book_id)
        if error:
            return error

        user_data = await User.get(user_id)
        if book_id in user_data.favourites:
            return RepositoryError(message=f"Book with id {book_id} is already in favourites")

        user_data.favourites.append(book_id)
        await user_data.save()
        return None

    async def remove_from_favourites(self, user_id, book_id: PydanticObjectId) -> RepositoryError | None:
        error = await _validate_user_and_book(user_id, book_id)
        if error:
            return error

        user_data = await User.get(user_id)
        if book_id not in user_data.favourites:
            return RepositoryError(message=f"Book with id {book_id} is not in favourites")

        user_data.favourites.remove(book_id)
        await user_data.save()
        return None
