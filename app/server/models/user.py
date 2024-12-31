from beanie import Document
from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import List, Optional

from app.server.models.book import Book
from app.server.models.collection import Collection
from  app.server.models.quote import Quote


class User(Document):
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    password: str
    userBooks: List[Book]
    collections: List[Collection]
    quotes: List[Quote]
    favourites: List[str]
    class Settings:
        name = "users"

class UpdateUser(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    userBooks: Optional[List[Book]]
    collection: Optional[List[Collection]]
    quotes: Optional[List[Quote]]
    favourites: Optional[List[str]]