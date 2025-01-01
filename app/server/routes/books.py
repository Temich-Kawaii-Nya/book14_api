from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.server.models.book import Book
from app.server.models.user import User

router = APIRouter()
#add new book to user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book_to_user(user_id: PydanticObjectId, book: Book):
    user_data = await User.get(user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    # if any(book.isnb == isnb for book in user_data.userBooks):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Book with ISNB {isnb} is already added to the user."
    #     )
    if not user_data.userBooks:
        raise HTTPException(
            status_code=status.HTTP_100_CONTINUE
        )
    user_data.userBooks.append(book)
    await user_data.save()


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_book_from_user(user_id: PydanticObjectId, book_id: PydanticObjectId):
    user_data = await User.get(user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    book_to_remove = next((book for book in user_data.userBooks if book.id == book_id), None)
    if not book_to_remove:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No book with id {book_id} belongs to user",
        )
    user_data.userBooks.remove(book_to_remove)
    await user_data.save()

@router.get("/{user_id}")
async def get_all_books(user_id: PydanticObjectId):
    user_data = await User.get(user_id)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found"
        )
    if not user_data.userBooks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} does not have any books"
        )
    return user_data.userBooks
