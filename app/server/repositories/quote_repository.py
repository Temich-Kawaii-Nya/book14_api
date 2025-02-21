from abc import ABC, abstractmethod
from typing import Optional, List

from beanie import PydanticObjectId
from datetime import datetime

from ..models.user import User
from ..models.quote import Quote
from .repository_error import RepositoryError


class IQuoteRepository(ABC):
    """
    Interface for managing quotes related to books.
    """
    @abstractmethod
    async def add_quote_to_book(self, user: User, book_id: PydanticObjectId, text: str, pages: int) -> RepositoryError | None:
        """
        Adds a quote to a specific book for a user.

        Args:
            user (User): The model of user.
            book_id (PydanticObjectId): The ID of the book.
            text (str): The text of the quote.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def update_quote(self, user: User, quote_id: PydanticObjectId, new_text: str, page: int) -> RepositoryError | None:
        """
        Updates the text of a specific quote.

        Args:
            user (User): The model of user.
            quote_id (PydanticObjectId): The ID of the quote.
            new_text (str): The new text for the quote.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def remove_quote_from_book(self, user: User, quote_id: PydanticObjectId) -> RepositoryError | None:
        """
        Removes a specific quote from a user's collection.

        Args:
            user (User): The model of user.
            quote_id (PydanticObjectId): The ID of the quote to remove.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def get_quote_by_id(self, user: User, quote_id: PydanticObjectId) -> Quote:
        """
        Retrieves all quotes for a specific book in the user's collection.

        Args:
            user (User): The model of user.
            quote_id (PydanticObjectId): The ID of the book.

        Returns:
            Quote: Returns quote model.
        """
        pass
    @abstractmethod
    async def get_quotes_for_book(self, user: User, book_id: PydanticObjectId) -> List[Quote] | RepositoryError:
        """
        Retrieves all quotes for a specific book in the user's collection.

        Args:
            user (User): The model of user.
            book_id (PydanticObjectId): The ID of the book.

        Returns:
            List[Quote] | RepositoryError: Returns a list of quotes or an error if the operation fails.
        """
        pass


class QuoteRepository(IQuoteRepository, ABC):
    """
    Implementation of the IQuoteRepository interface for managing quotes.
    """
    async def add_quote_to_book(self, user: User, book_id: PydanticObjectId, text: str, pages: int) -> Quote:
        if not any(book.id == book_id for book in user.userBooks):
            raise RepositoryError(message=f"Book with id {book_id} not found in user's book list", statuscode=404)
        new_quote = Quote(book_id=book_id, text=text, created_at=datetime.now(), pages = pages)
        user.quotes.append(new_quote)
        await user.save()
        return new_quote

    async def update_quote(self, user: User, quote_id: PydanticObjectId, new_text: str, pages: int):
        for quote in user.quotes:
            if quote.id == quote_id:
                quote.text = new_text
                quote.pages = pages
                await user.save()
                return
        raise RepositoryError(message=f"Quote with id {quote_id} not found", statuscode=404)

    async def remove_quote_from_book(self, user: User, quote_id: PydanticObjectId):
        for quote in user.quotes:
            if quote.id == quote_id:
                user.quotes.remove(quote)
                await user.save()
                return
        raise RepositoryError(message=f"Quote with id {quote_id} not found", statuscode=404)

    async def get_quote_by_id(self, user: User, quote_id: PydanticObjectId) -> Quote:
        quote = next((quote for quote in user.quotes if quote.id == quote_id), None)
        if not quote:
            raise RepositoryError(message=f"Quote with id {quote_id} not found.", statuscode=404)
        return quote

    async def get_quotes_for_book(self, user: User, book_id: PydanticObjectId) -> List[Quote]:
        quotes_for_book = [quote for quote in user.quotes if quote.book_id == book_id]
        return quotes_for_book
