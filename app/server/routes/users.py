from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.server.models.user import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    await user.insert()
@router.get("/{user_id}")
async def read_user(user_id: PydanticObjectId):
    user_data = await User.get(user_id)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found"
        )
    return user_data


