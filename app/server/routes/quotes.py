from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.server.middlewares.token_validation import validate_token
from app.server.models.quote import CreateQuote
from app.server.models.user import User
from app.server.repositories.quote_repository import QuoteRepository
from app.server.repositories.repository_error import RepositoryError

router = APIRouter()
quotes_repo = QuoteRepository()

@router.get("/", status_code=status.HTTP_200_OK)
async def get_quotes(book_id: PydanticObjectId, current_user: Annotated[User, Depends(validate_token)]):
    try:
        quotes = await quotes_repo.get_quotes_for_book(current_user, book_id)
        return {"status": "ok", "quotes": quotes}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
@router.get("/{quote_id}", status_code=status.HTTP_200_OK)
async def get_quotes(quote_id: PydanticObjectId, current_user: Annotated[User, Depends(validate_token)]):
    try:
        quote = await quotes_repo.get_quote_by_id(current_user, quote_id)
        return {"status": "ok", "quotes": quote}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_quote(quote: CreateQuote, current_user: Annotated[User, Depends(validate_token)]):
    try:
        created_quote = await quotes_repo.add_quote_to_book(current_user, quote.book_id, quote.text)
        return {"status": "ok", "quote": created_quote}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.put("/{quote_id}", status_code=status.HTTP_200_OK)
async def update_quote(quote_id: PydanticObjectId, new_text: str, current_user: Annotated[User, Depends(validate_token)]):
    try:
        quote = await quotes_repo.update_quote(current_user, quote_id, new_text)
        return {"status": "ok", "quote": quote}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@router.delete("/{quote_id}", status_code=status.HTTP_200_OK)
async def delete_quote(quote_id: PydanticObjectId,
                       current_user: Annotated[User, Depends(validate_token)]):
    try:
        quote = await quotes_repo.remove_quote_from_book(current_user, quote_id)
        return {"status": "ok", "quote": quote}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)