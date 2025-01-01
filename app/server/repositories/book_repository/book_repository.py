from abc import ABC
from typing import List

from beanie import PydanticObjectId

from app.server.models.book import Book
from app.server.models.quote import Quote
from app.server.models.user import User
from app.server.repositories.book_repository.book_repository_interface import IBookRepository
from app.server.repositories.repository_error import RepositoryError


class BookRepository(IBookRepository, ABC):
    async def add_book_to_user(self, user_id: PydanticObjectId, book: Book):
        user_data = await User.get(user_id)
        if not user_data:
            error = RepositoryError(message=f"No user with id {user_id}.")
            return error
        if any(existing_book.isnb == book.isnb for existing_book in user_data.userBooks):
            error = RepositoryError(message=f"Book with ISNB {book.isnb} is already added to the user.")
            return error
        user_data.userBooks.append(book)
        await user_data.save()
        return None

    async def delete_book_from_user(self, user_id: PydanticObjectId, book_id: PydanticObjectId):
        user_data = await User.get(user_id)
        if not user_data:
            error = RepositoryError(message=f"No user with id {user_id}.")
            return error
        book_to_remove = next((book for book in user_data.userBooks if book.id == book_id))
        if not book_to_remove:
            error = RepositoryError(message=f"No book with id {book_id} belongs to user.")
            return error
        user_data.userBooks.remove(book_to_remove)
        await user_data.save()
        return None

    async def get_all_books(self, user_id: PydanticObjectId) -> (RepositoryError, List[Book]):
        user_data = await User.get(user_id)
        if not user_data:
            error = RepositoryError(message=f"User with id {user_id} not found")
            return error, None
        if not user_data.userBooks:
            error = RepositoryError(message=f"User with id {user_id} does not have any books.")
            return error, None
        return None, user_data.userBooks

    async def get_book_by_id(self, user_id, book_id: PydanticObjectId) -> (RepositoryError, Book):
        user_data = await User.get(user_id)
        if not user_data:
            error = RepositoryError(message=f"User with id {user_id} not found")
            return error, None
        if not user_data.userBooks:
            error = RepositoryError(message=f"User with id {user_id} does not have any books.")
            return error, None
        book = next((book for book in user_data.userBooks if book.id == book_id))
        return None, book


    async def update_book(self, user_id, book_id: PydanticObjectId, new_book_data: Book) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            error = RepositoryError(message=f"User with id {user_id} not found")
            return error
        if not user_data.userBooks:
            error = RepositoryError(message=f"User with id {user_id} does not have any books.")
            return error
        for index, book in enumerate(user_data.userBooks):
            if book.id == book_id:
                user_data.userBooks[index] = new_book_data
                await user_data.save()
                return None
        error = RepositoryError(message=f"Book with id {book_id} not found for user {user_id}.")
        return error

    # async def add_quote_to_book(self, user_id, book_id: PydanticObjectId, quote: Quote):
    #     user_data = await User.get(user_id)
    #     if not user_data:
    #         error = RepositoryError(message=f"User with id {user_id} not found")
    #         return error

    # @abstractmethod
    # async def add_to_collection(self, user_id, book_id, collection_id: PydanticObjectId):
    #     pass