from abc import ABC, abstractmethod
from typing import List

from beanie import PydanticObjectId

from app.server.models.book import Book, UpdateBook
from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError


class IBookRepository(ABC):
    """
    Interface for a book repository that defines methods for managing books within a user's account.
    """
    @abstractmethod
    async def add_book_to_user(self, user: User, book: Book) -> PydanticObjectId:
        """
        Add a book to a user's collection.

        :param user: The model of user.
        :param book: The book model to add.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_book_from_user(self, user: User, book_id: PydanticObjectId) -> PydanticObjectId:
        """
        Remove a book from a user's collection.

        :param user: The model of user.
        :param book_id: The ID of the book to remove.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def get_all_books(self, user: User) -> List[Book]:
        """
        Retrieve all books in a user's collection.

        :param user: The model of user.
        :return: A list of book models or a RepositoryError if an error occurs.
        """
        pass

    @abstractmethod
    async def get_book_by_id(self, user: User, book_id: PydanticObjectId) -> Book:
        """
        Retrieve a specific book by its ID.

        :param user: The model of user.
        :param book_id: The ID of the book.
        :return: The book or a RepositoryError if an error occurs.
        """
        pass

    @abstractmethod
    async def update_book(self, user: User, book_id: PydanticObjectId, new_book_data: Book) -> Book:
        """
        Update the data of a specific book in a user's collection.

        :param user: The model of user.
        :param book_id: The ID of the book to update.
        :param new_book_data: New book model.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

class BookRepository(IBookRepository, ABC):
    async def add_book_to_user(self, user: User, book: Book):
        if any(existing_book.isnb == book.isnb for existing_book in user.userBooks):
            raise RepositoryError(message=f"Book with ISNB {book.isnb} is already added to the user.")
        user.userBooks.append(book)
        await user.save()

    async def delete_book_from_user(self, user: User, book_id: PydanticObjectId)-> PydanticObjectId:
        book_to_remove = next((book for book in user.userBooks if book.id == book_id), None)
        if not book_to_remove:
            raise RepositoryError(message=f"No book with id {book_id} belongs to user.", statuscode=404)
        user.userBooks.remove(book_to_remove)
        await user.save()
        return book_id

    async def get_all_books(self, user: User) -> List[Book]:
        return user.userBooks

    async def get_book_by_id(self, user: User, book_id: PydanticObjectId) -> Book:
        book = next((book for book in user.userBooks if book.id == book_id), None)
        if not book:
            raise RepositoryError(message=f"Book with id {book_id} not found for user {user.id}.", statuscode=404)
        return book

    async def update_book(self, user: User, book_id: PydanticObjectId, new_book_data: UpdateBook) -> Book:
        for index, book in enumerate(user.userBooks):
            if book.id == book_id:
                updated_book = user.userBooks[index].model_copy(update=new_book_data.model_dump(exclude_unset=True))
                user.userBooks[index] = updated_book
                await user.save()
                return updated_book
        raise RepositoryError(message=f"Book with id {book_id} not found for user {user.id}.", statuscode=404)