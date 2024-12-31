from fastapi import APIRouter, HTTPException, status

from app.server.models.user import User

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    await user.insert()