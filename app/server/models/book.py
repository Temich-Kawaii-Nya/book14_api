from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.server.models.description import Description


class Book(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    isnb: str
    start_read_date: datetime
    end_read_date: datetime
    description: Description
    rating: int

class UpdateBook(BaseModel):
    """
        UpdateBook Model

        Represents the data structure for updating a book's information.
        This model allows partial updates, where only the provided fields
        will be updated. All fields are optional.

        Attributes:
            isnb (Optional[str]):
                The International Standard Book Number (ISBN) for the book.
                If provided, it should be a valid string representing the book's unique identifier.

            start_read_date (Optional[datetime]):
                The date when the user started reading the book. Must be a valid datetime object.

            end_read_date (Optional[datetime]):
                The date when the user finished reading the book. Must be a valid datetime object.

            description (Optional[Description]):
                The model of desctiption for book.

            rating (Optional[int]):
                The user’s rating for the book. Must be an integer from 0 to 100.

        Usage Example:
            >>> update_data = UpdateBook(
            >>>     end_read_date= datetime(2005, 1, 5, 17, 14, 35)
            >>>     rating=5,
            >>> )
        """
    isnb: Optional[str] = None
    start_read_date: Optional[datetime]= None
    end_read_date: Optional[datetime]= None
    description: Optional[Description]= None
    rating: Optional[int]= None