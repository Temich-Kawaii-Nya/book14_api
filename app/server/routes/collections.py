from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends

from app.server.models.book import Book
from app.server.models.user import User
from app.server.models.collection import Collection
from app.server.middlewares.token_validation import validate_token


router = APIRouter()
#add new collection to user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book_to_user(collection: Collection, current_user: Annotated[User, Depends(validate_token)]):
    return  current_user
    # if not user_data:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"User with id {user_id} not found",
    #     )
    # # if any(book.isnb == isnb for book in user_data.userBooks):
    # #     raise HTTPException(
    # #         status_code=status.HTTP_400_BAD_REQUEST,
    # #         detail=f"Book with ISNB {isnb} is already added to the user."
    # #     )
    # if not user_data.userBooks:
    #     raise HTTPException(
    #         status_code=status.HTTP_100_CONTINUE
    #     )
    # user_data.userBooks.append(book)
    # await user_data.save()

