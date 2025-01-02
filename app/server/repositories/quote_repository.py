from abc import ABC, abstractmethod
from typing import Optional, List

from beanie import PydanticObjectId
from datetime import datetime

from app.server.models.user import User
from app.server.models.quote import Quote
from app.server.repositories.repository_error import RepositoryError


class IQuoteRepository(ABC):
    """
    Interface for managing quotes related to books.
    """
    @abstractmethod
    async def add_quote_to_book(self, user_id: PydanticObjectId, book_id: PydanticObjectId, text: str) -> RepositoryError | None:
        """
        Adds a quote to a specific book for a user.

        Args:
            user_id (PydanticObjectId): The ID of the user.
            book_id (PydanticObjectId): The ID of the book.
            text (str): The text of the quote.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def update_quote(self, user_id: PydanticObjectId, quote_id: PydanticObjectId, new_text: str) -> RepositoryError | None:
        """
        Updates the text of a specific quote.

        Args:
            user_id (PydanticObjectId): The ID of the user.
            quote_id (PydanticObjectId): The ID of the quote.
            new_text (str): The new text for the quote.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def remove_quote_from_book(self, user_id: PydanticObjectId, quote_id: PydanticObjectId) -> RepositoryError | None:
        """
        Removes a specific quote from a user's collection.

        Args:
            user_id (PydanticObjectId): The ID of the user.
            quote_id (PydanticObjectId): The ID of the quote to remove.

        Returns:
            RepositoryError | None: Returns an error if the operation fails, otherwise None.
        """
        pass

    @abstractmethod
    async def get_quotes_for_book(self, user_id: PydanticObjectId, book_id: PydanticObjectId) -> List[Quote] | RepositoryError:
        """
        Retrieves all quotes for a specific book in the user's collection.

        Args:
            user_id (PydanticObjectId): The ID of the user.
            book_id (PydanticObjectId): The ID of the book.

        Returns:
            List[Quote] | RepositoryError: Returns a list of quotes or an error if the operation fails.
        """
        pass


class QuoteRepository(IQuoteRepository):
    """
    Implementation of the IQuoteRepository interface for managing quotes.
    """
    async def add_quote_to_book(self, user_id: PydanticObjectId, book_id: PydanticObjectId, text: str) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with id {user_id} not found")

        if not any(book.id == book_id for book in user_data.userBooks):
            return RepositoryError(message=f"Book with id {book_id} not found in user's book list")

        new_quote = Quote(book_id=str(book_id), text=text, created_at=datetime.utcnow())
        user_data.quotes.append(new_quote)
        await user_data.save()
        return None

    async def update_quote(self, user_id: PydanticObjectId, quote_id: PydanticObjectId, new_text: str) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with id {user_id} not found")

        for quote in user_data.quotes:
            if quote.id == quote_id:
                quote.text = new_text
                await user_data.save()
                return None

        return RepositoryError(message=f"Quote with id {quote_id} not found")

    async def remove_quote_from_book(self, user_id: PydanticObjectId, quote_id: PydanticObjectId) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with id {user_id} not found")

        for quote in user_data.quotes:
            if quote.id == quote_id:
                user_data.quotes.remove(quote)
                await user_data.save()
                return None

        return RepositoryError(message=f"Quote with id {quote_id} not found")

    async def get_quotes_for_book(self, user_id: PydanticObjectId, book_id: PydanticObjectId) -> List[Quote] | RepositoryError:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with id {user_id} not found")

        quotes_for_book = [quote for quote in user_data.quotes if quote.book_id == str(book_id)]
        return quotes_for_book
