from abc import ABC, abstractmethod
from beanie import PydanticObjectId
from app.server.models.book import Book
from typing import List

from app.server.models.quote import Quote
from app.server.repositories.repository_error import Result


class IBookRepository(ABC):
    @abstractmethod
    async def add_book_to_user(self, user_id: PydanticObjectId, book: Book):
        pass
    @abstractmethod
    async def delete_book_from_user(self, user_id, book_id: PydanticObjectId):
        pass
    @abstractmethod
    async def get_all_books(self, user_id: PydanticObjectId) -> List[Book]:
        pass
    @abstractmethod
    async def get_book_by_id(self, user_id, book_id: PydanticObjectId) -> Book:
        pass
    @abstractmethod
    async def update_book(self, user_id, book_id: PydanticObjectId, new_book_data: Book):
        pass
    @abstractmethod
    async def add_quote_to_book(self, user_id, book_id: PydanticObjectId, quote: Quote):
        pass
    @abstractmethod
    async def add_to_collection(self, user_id, book_id, collection_id: PydanticObjectId):
        pass
