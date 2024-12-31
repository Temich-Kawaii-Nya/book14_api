from typing import List, Optional
from beanie import Document
from pydantic import BaseModel


class Collection(Document):
    collection_name: str
    books: List[str]
class UpdateCollection(BaseModel):
    collection_name: Optional[str]
    books: Optional[List[str]]
