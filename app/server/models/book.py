from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel

from app.server.models.description import Description


class Book(Document):
    isnb: str
    start_read_date: datetime
    end_read_date: datetime
    description: Description
    rating: int
class UpdateBook(BaseModel):
    isnb: Optional[str]
    start_read_date: Optional[datetime]
    end_read_date: Optional[datetime]
    description: Optional[Description]
    rating: Optional[int]