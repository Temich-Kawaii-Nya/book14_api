from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import EmailStr, BaseModel, Field

from .book import Book
from .collection import Collection
from .quote import Quote


class User(Document):
    username: str = Field(..., min_length=3)
    email: EmailStr = Field()
    password: str = Field(..., min_length=6)
    created_at: datetime
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

class UserResponse(BaseModel):
    created_at: datetime
    userBooks: List[Book]
    collections: List[Collection]
    quotes: List[Quote]
    favourites: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


class SignupData(BaseModel):
    username: str
    password: str
    email: EmailStr