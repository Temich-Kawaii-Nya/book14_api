from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel


class Quote(Document):
    book_id: str
    text: str
    created_at: datetime
class UpdateQuote(BaseModel):
    text: Optional[str]
