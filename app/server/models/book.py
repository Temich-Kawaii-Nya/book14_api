from typing import Optional, Annotated
from pydantic import BaseModel, PlainSerializer
from app.server.models.description import Description
from beanie import Document, PydanticObjectId
from datetime import datetime

SerializedObjectId = Annotated[
    PydanticObjectId,
    PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]

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