from abc import ABC, abstractmethod

from beanie import PydanticObjectId

from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError


class IFavouriteRepository(ABC):
    """
    Abstract base class for a repository that manages user book favourites.
    Defines the interface for adding and removing books from a user's favourites.
    """

    @abstractmethod
    async def add_to_favourites(self, user: User, book_id: PydanticObjectId) -> RepositoryError | None:
        """
        Adds a book to the user's favourites list.

        Args:
            user (User): The model of user.
            book_id (PydanticObjectId): The ID of the book to be added to favourites.

        Returns:
            RepositoryError: If fails, returns an error. Otherwise, returns None.
        """
        pass

    @abstractmethod
    async def remove_from_favourites(self, user: User, book_id: PydanticObjectId) -> RepositoryError | None:
        """
        Removes a book from the user's favourites list.

        Args:
            user (User): The model of user.
            book_id (PydanticObjectId): The ID of the book to be removed from favourites.

        Returns:
            RepositoryError: If fails, returns an error. Otherwise, returns None.
        """
        pass

class FavouriteRepository(IFavouriteRepository, ABC):
    async def add_to_favourites(self, user: User, book_id: PydanticObjectId):
        if not any(book.id == book_id for book in user.userBooks):
            raise RepositoryError(message=f"Book with id {book_id} not found in user's book list", statuscode=404)
        if book_id in user.favourites:
            return RepositoryError(message=f"Book with id {book_id} is already in favourites", statuscode=400)
        user.favourites.append(book_id.__str__())
        await user.save()

    async def remove_from_favourites(self, user: User, book_id: PydanticObjectId) -> RepositoryError | None:
        if not any(book.id == book_id for book in user.userBooks):
            raise RepositoryError(message=f"Book with id {book_id} not found in user's book list", statuscode=404)
        if book_id not in user.favourites:
            return RepositoryError(message=f"Book with id {book_id} is not in favourites")
        user.favourites.remove(book_id.__str__())
        await user.save()
