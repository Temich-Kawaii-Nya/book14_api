import logging
from abc import ABC, abstractmethod
from typing import List

import pydantic_core
from beanie import PydanticObjectId
from pydantic.deprecated.json import pydantic_encoder

from app.server.models.book import Book, UpdateBook
from app.server.models.description import Description
from app.server.models.quote import Quote
from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError

class IBookRepository(ABC):
    """
    Interface for a book repository that defines methods for managing books within a user's account.
    """
    @abstractmethod
    async def add_book_to_user(self, user_id: PydanticObjectId, book: Book) -> PydanticObjectId:
        """
        Add a book to a user's collection.

        :param user_id: The ID of the user.
        :param book: The book model to add.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_book_from_user(self, user_id, book_id: PydanticObjectId) -> PydanticObjectId:
        """
        Remove a book from a user's collection.

        :param user_id: The ID of the user.
        :param book_id: The ID of the book to remove.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def get_all_books(self, user_id: PydanticObjectId) -> List[Book]:
        """
        Retrieve all books in a user's collection.

        :param user_id: The ID of the user.
        :return: A list of book models or a RepositoryError if an error occurs.
        """
        pass

    @abstractmethod
    async def get_book_by_id(self, user_id, book_id: PydanticObjectId) -> Book:
        """
        Retrieve a specific book by its ID.

        :param user_id: The ID of the user.
        :param book_id: The ID of the book.
        :return: The book or a RepositoryError if an error occurs.
        """
        pass

    @abstractmethod
    async def update_book(self, user_id, book_id: PydanticObjectId, new_book_data: Book) -> Book:
        """
        Update the data of a specific book in a user's collection.

        :param user_id: The ID of the user.
        :param book_id: The ID of the book to update.
        :param new_book_data: New book model.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

class BookRepository(IBookRepository, ABC):
    async def add_book_to_user(self, user_id: PydanticObjectId, book: Book):
        user_data = await User.get(user_id)
        if not user_data:
            raise RepositoryError(message=f"No user with id {user_id}.")
        if any(existing_book.isnb == book.isnb for existing_book in user_data.userBooks):
            raise RepositoryError(message=f"Book with ISNB {book.isnb} is already added to the user.")
        user_data.userBooks.append(book)
        await user_data.save()

    async def delete_book_from_user(self, user_id: PydanticObjectId, book_id: PydanticObjectId)-> PydanticObjectId:
        user_data = await User.get(user_id)
        if not user_data:
            raise RepositoryError(message=f"No user with id {user_id}.", statuscode=404)
        book_to_remove = next((book for book in user_data.userBooks if book.id == book_id), None)
        if not book_to_remove:
            raise RepositoryError(message=f"No book with id {book_id} belongs to user.", statuscode=404)
        user_data.userBooks.remove(book_to_remove)
        await user_data.save()
        return book_id

    async def get_all_books(self, user_id: PydanticObjectId) -> List[Book]:
        user_data = await User.get(user_id)
        if not user_data:
            raise RepositoryError(message=f"User with id {user_id} not found", statuscode=404)
        if not user_data.userBooks:
            raise RepositoryError(message=f"User with id {user_id} not found", statuscode=404)
        return user_data.userBooks

    async def get_book_by_id(self, user_id, book_id: PydanticObjectId) -> Book:
        user_data = await User.get(user_id)
        if not user_data:
            raise RepositoryError(message=f"User with id {user_id} not found", statuscode=404)
        if not user_data.userBooks:
            raise RepositoryError(message=f"User with id {user_id} does not have any books.", statuscode=404)
        book = next((book for book in user_data.userBooks if book.id == book_id), None)
        if not book:
            raise RepositoryError(message=f"Book with id {book_id} not found for user {user_id}.", statuscode=404)
        return book

    async def update_book(self, user_id, book_id: PydanticObjectId, new_book_data: UpdateBook) -> Book:
        user_data = await User.get(user_id)
        if not user_data:
            raise RepositoryError(message=f"User with id {user_id} not found", statuscode=404)
        for index, book in enumerate(user_data.userBooks):
            if book.id == book_id:
                updated_book = user_data.userBooks[index].model_copy(update=new_book_data.model_dump(exclude_unset=True))
                user_data.userBooks[index] = updated_book
                await user_data.save()
                return updated_book
        raise RepositoryError(message=f"Book with id {book_id} not found for user {user_id}.", statuscode=404)