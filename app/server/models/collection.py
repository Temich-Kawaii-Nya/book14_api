from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, Field


class Collection(Document):
    collection_name: str = Field(..., min_length=1)
    books: List[str]
class UpdateCollection(BaseModel):
    collection_name: Optional[str]
    books: Optional[List[str]]
