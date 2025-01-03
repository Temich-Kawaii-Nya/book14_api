from abc import ABC, abstractmethod
from typing import List

from beanie import PydanticObjectId

from app.server.models.collection import Collection
from app.server.models.user import User
from app.server.repositories.repository_error import RepositoryError


class ICollectionRepository(ABC):
    """
    Interface for managing book collections.
    """

    @abstractmethod
    async def create_collection(self, user_id: PydanticObjectId, collection_name: str) -> RepositoryError | None:
        """
        Create a new collection.

        :param user_id: The ID of the user.
        :param collection_name: The name of the collection.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId) -> RepositoryError | None:
        """
        Delete a collection.

        :param user_id: The ID of the user.
        :param collection_id: The ID of the collection.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def add_book_to_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId, book_id: str) -> RepositoryError | None:
        """
        Add a book to a collection.

        :param user_id: The ID of the user.
        :param collection_id: The ID of the collection.
        :param book_id: The ID of the book.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def remove_book_from_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId, book_id: str) -> RepositoryError | None:
        """
        Remove a book from a collection.

        :param user_id: The ID of the user.
        :param collection_id: The ID of the collection.
        :param book_id: The ID of the book.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass

    @abstractmethod
    async def update_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId, new_name: str) -> RepositoryError | None:
        """
        Update collection data.

        :param user_id: The ID of the user.
        :param collection_id: The ID of the collection.
        :param new_name: The new name of the collection.
        :return: RepositoryError if an error occurs, otherwise None.
        """
        pass


class CollectionRepository(ICollectionRepository):
    """
    Implementation of the ICollectionRepository interface for managing collections.
    """

    async def create_collection(self, user: User, collection_name: str) -> RepositoryError | None:
        new_collection = Collection(collection_name=collection_name, books=[])
        user.collections.append(new_collection)
        await user.save()
        return None

    async def delete_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with ID {user_id} not found.")
        collection_to_remove = next((col for col in user_data.collections if col.id == collection_id), None)
        if not collection_to_remove:
            return RepositoryError(message=f"Collection with ID {collection_id} not found.")
        user_data.collections.remove(collection_to_remove)
        await user_data.save()
        return None

    async def add_book_to_collection(self, user: User, collection_id: int, book_id: str) -> RepositoryError | None:
        collection = user.collections[collection_id]
        if not collection:
            return RepositoryError(message=f"Collection with ID {collection_id} not found.")
        if book_id in collection.books:
            return RepositoryError(message=f"Book with ID {book_id} is already in the collection.")
        collection.books.append(book_id)
        await user.save()
        return None

    async def remove_book_from_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId, book_id: str) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with ID {user_id} not found.")
        collection = next((col for col in user_data.collections if col.id == collection_id), None)
        if not collection:
            return RepositoryError(message=f"Collection with ID {collection_id} not found.")
        if book_id not in collection.books:
            return RepositoryError(message=f"Book with ID {book_id} is not in the collection.")
        collection.books.remove(book_id)
        await user_data.save()
        return None

    async def update_collection(self, user_id: PydanticObjectId, collection_id: PydanticObjectId, new_name: str) -> RepositoryError | None:
        user_data = await User.get(user_id)
        if not user_data:
            return RepositoryError(message=f"User with ID {user_id} not found.")
        collection = next((col for col in user_data.collections if col.id == collection_id), None)
        if not collection:
            return RepositoryError(message=f"Collection with ID {collection_id} not found.")
        collection.collection_name = new_name
        await user_data.save()
        return None
