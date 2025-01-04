import logging
from http import HTTPStatus
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends

from app.server.middlewares.token_validation import validate_token
from app.server.models.book import Book, UpdateBook
from app.server.models.user import User
from app.server.repositories.book_repository import BookRepository
from app.server.repositories.repository_error import RepositoryError

router = APIRouter()
book_rep_instance = BookRepository()

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
        await book_rep.add_book_to_user(user.id, book)
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
        await book_rep.delete_book_from_user(user.id, book_id)
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
        book = await book_rep.update_book(user.id, book_id, new_data)
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
        books = await book_rep.get_all_books(user.id)
        return books
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
        books = await book_rep.get_all_books(user.id)
        return books
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

