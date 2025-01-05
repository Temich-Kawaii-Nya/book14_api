from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.server.middlewares.token_validation import validate_token
from app.server.models.user import User
from app.server.repositories.collection_repository import CollectionRepository
from app.server.repositories.repository_error import RepositoryError

router = APIRouter()
collection_repo = CollectionRepository()
#add new collection to user

@router.get("/", status_code=status.HTTP_200_OK)
async def get_collections(current_user: Annotated[User, Depends(validate_token)]):
    try:
        collections = await collection_repo.get_collections(current_user)
        return {"Success": True, "collections": collections}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.get("/{collection_id}", status_code=status.HTTP_200_OK)
async def get_collection(collection_id: int, current_user: Annotated[User, Depends(validate_token)]):
    try:
        collection = await collection_repo.get_collection(current_user, collection_id)
        return {"Success": True, "collection": collection}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_collection(collection_name: str, current_user: Annotated[User, Depends(validate_token)]):
    try:
        await collection_repo.create_collection(current_user, collection_name)
        return {"Success": True}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/add_book/{collection_id}")
async def add_book_to_collection(collection_id: int, book_id: str, current_user: Annotated[User, Depends(validate_token)]):
    try:
        await  collection_repo.add_book_to_collection(current_user, collection_id, book_id)
        return {"Success": True}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.put("/{collection_id}")
async def update_collection(collection_id: int, collection_name: str, current_user: Annotated[User, Depends(validate_token)]):
    try:
        await collection_repo.update_collection(current_user, collection_id, collection_name)
        return {"Success": True}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.post("/remove_book/{collection_id}")
async def remove_book_from_collection(collection_id: int, book_id: str, current_user: Annotated[User, Depends(validate_token)]):
    try:
        await  collection_repo.remove_book_from_collection(current_user, collection_id, book_id)
        return {"Success": True}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

@router.delete("/{collection_id}")
async def delete_collection(collection_id: int, current_user: Annotated[User, Depends(validate_token)]):
    try:
        await  collection_repo.delete_collection(current_user, collection_id)
        return {"Success": True}
    except RepositoryError as e:
        raise HTTPException(status_code=e.code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
