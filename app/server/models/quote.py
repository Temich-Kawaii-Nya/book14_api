from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field

class Quote(Document):
    book_id: str = Field()
    text: str = Field(..., min_length=1)
    created_at: datetime
class UpdateQuote(BaseModel):
    text: Optional[str]

class CreateQuote(BaseModel):
    book_id: str
    text: str