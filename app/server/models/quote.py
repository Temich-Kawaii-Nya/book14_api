from datetime import datetime
from typing import Optional, Annotated

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, PlainSerializer

SerializedObjectId = Annotated[
    PydanticObjectId,
    PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]

class Quote(Document):
    book_id: str = Field()
    text: str = Field(..., min_length=1)
    created_at: datetime
class UpdateQuote(BaseModel):
    text: Optional[str]
