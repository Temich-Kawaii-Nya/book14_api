import logging
from datetime import datetime
from typing import Annotated

from beanie.odm.utils.pydantic import parse_object_as
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.server.middlewares.token_validation import validate_token, hash_password, create_access_token, verify_password
from app.server.models.user import User, SignupData, Token
from app.server.repositories.user_repository import UserRepository

router = APIRouter()

user_rep_instance = UserRepository()

logging.basicConfig(level=logging.INFO)

def get_user_repository() -> UserRepository:
    return user_rep_instance
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(signup_data: SignupData, user_rep = Depends(get_user_repository)):
    user_with_username = await user_rep.get_user_by_name(username=signup_data.username)
    if user_with_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    user_with_email = await user_rep.get_user_by_email(email=signup_data.email)
    if user_with_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken")
    hashed_password = hash_password(signup_data.password)
    user = User(
        username=signup_data.username,
        email=signup_data.email,
        password=hashed_password,
        created_at=datetime.utcnow(),
        userBooks=[],
        collections=[],
        quotes=[],
        favourites=[])
    await user_rep.add_user(user=user)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_rep = Depends(get_user_repository)):
    try:
        logging.info("Attempting to find user by email")
        user_dict = await user_rep.get_user_by_email(email=parse_object_as(EmailStr, form_data.username))
        if not user_dict:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not verify_password(form_data.password, user_dict.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        logging.info(user_dict.id)
        access_token = create_access_token(data={"sub": user_dict.username})

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(current_user: Annotated[User, Depends(validate_token)]):
    return current_user