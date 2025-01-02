from typing import List, Optional, Annotated
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, PlainSerializer

SerializedObjectId = Annotated[
    PydanticObjectId,
    PlainSerializer(lambda x: str(x), return_type=str, when_used='json')
]

class Collection(Document):
    collection_name: str = Field(..., min_length=1)
    books: List[str]
class UpdateCollection(BaseModel):
    collection_name: Optional[str]
    books: Optional[List[str]]
