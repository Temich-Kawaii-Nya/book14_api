from typing import Annotated

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Depends

from app.server.models.book import Book
from app.server.models.user import User
from app.server.models.collection import Collection
from app.server.middlewares.token_validation import validate_token
from app.server.repositories.collection_repository import CollectionRepository

router = APIRouter()
collection_repo = CollectionRepository()
#add new collection to user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_collection(collection_name: str, current_user: Annotated[User, Depends(validate_token)]):
    await collection_repo.create_collection(current_user, collection_name)
    return {"Success": True}

@router.post("/add_book/{collection_id}")
async def add_book_to_collection(collection_id: int, book_id: str, current_user: Annotated[User, Depends(validate_token)]):
    await  collection_repo.add_book_to_collection(current_user, collection_id, book_id)
    return {"Success": True}
