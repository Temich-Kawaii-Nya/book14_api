from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field


class Description(Document):
    title: str = Field(..., min_length=1)
    description: str
    author_name: str
    publisher_name: str
    publishing_date: datetime
    cover_url: str
class UpdateDescription(BaseModel):
    title: Optional[str]
    description: Optional[str]
    author_name: Optional[str]
    publisher_name: Optional[str]
    publishing_date: Optional[datetime]
    cover_url: Optional[str]
