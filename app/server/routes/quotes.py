from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.server.middlewares.token_validation import validate_token
from app.server.models.quote import CreateQuote
from app.server.models.user import User
from app.server.repositories.quote_repository import QuoteRepository
from app.server.repositories.repository_error import RepositoryError

router = APIRouter()
quotes_repo = QuoteRepository()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_quote(quote: CreateQuote, current_user: Annotated[User, Depends(validate_token)]):
    try:
        created_quote = await quotes_repo.add_quote_to_book(current_user, quote.book_id, quote.text)
        return {"status": "ok", "quote": created_quote}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)