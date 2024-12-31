from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.server.models.user import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    await user.insert()
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def read_user(user_id: PydanticObjectId):
    return await User.get(user_id)