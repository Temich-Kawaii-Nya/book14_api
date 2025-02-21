from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Quote(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    book_id: PydanticObjectId = Field()
    text: str = Field(..., min_length=1)
    pages: int
    created_at: datetime

class UpdateQuote(BaseModel):
    text: Optional[str]
    pages: Optional[int]

class CreateQuote(BaseModel):
    book_id: PydanticObjectId
    text: str
    pages: int