from typing import Annotated, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends, Query

from ..middlewares.token_validation import validate_token
from ..models.book import Book, UpdateBook
from ..models.user import User
from ..repositories.book_repository import BookRepository
from ..repositories.book_search_context import IGoogleBooksContext, SearchBookModel
from ..repositories.repository_error import RepositoryError

router = APIRouter()
book_rep_instance = BookRepository()
book_search = IGoogleBooksContext()
def get_book_repository() -> BookRepository:
    return book_rep_instance

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_book_to_user(
        user: Annotated[User, Depends(validate_token)],
        book: Book,
        book_rep: BookRepository = Depends(get_book_repository
    )):
    """
    :param user: The model of current user
    :param book: The model of book
    :param book_rep: Repository class for books
    :returns book: Added book
    """
    try:
        await book_rep.add_book_to_user(user, book)
        return book
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_book_from_user(
        user: Annotated[User, Depends(validate_token)],
        book_id: PydanticObjectId,
        book_rep: BookRepository = Depends(get_book_repository)):
    """
        :param user: The model of current user
        :param book_id: ID of book
        :param book_rep: Repository class for books
        :returns book: ID of removed book
    """
    try:
        await book_rep.delete_book_from_user(user, book_id)
        return book_id
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
@router.put("/{book_id}", status_code=status.HTTP_200_OK)
async def update_book_from_user(
        user: Annotated[User, Depends(validate_token)],
        book_id: PydanticObjectId,
        new_data: UpdateBook,
        book_rep: BookRepository = Depends(get_book_repository)):
    """
        :param user: The model of current user
        :param book_id: ID of book
        :param new_data: New book data
        :param book_rep: Repository class for books
        :returns book: New book data
    """
    try:
        book = await book_rep.update_book(user, book_id, new_data)
        return book
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.get("/")
async def get_all_books(
        user: Annotated[User, Depends(validate_token)],
        book_rep: BookRepository = Depends(get_book_repository)):
    """
        :param user: The model of current user
        :param book_rep: Repository class for books
        :returns List[book]: List of user books
    """
    try:
        books = await book_rep.get_all_books(user)
        return books
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
@router.get("/{book_id}")
async def get_book(
        user: Annotated[User, Depends(validate_token)],
        book_id: PydanticObjectId,
        book_rep: BookRepository = Depends(get_book_repository)):
    """
        :param user: The model of current user
        :param book_id: The id of the book
        :param book_rep: Repository class for books
        :returns book: The model of book
    """
    try:
        book = await book_rep.get_book_by_id(user, book_id)
        return book
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
@router.post("/find/")
async def find_book(
        user: Annotated[User, Depends(validate_token)],
        phrase: Optional[str] = Query(default="", alias="phrase")):
    try:
        book = await book_search.find_book(phrase)
        return book
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
