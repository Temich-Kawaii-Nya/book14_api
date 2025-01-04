import logging
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from beanie.odm.utils.pydantic import parse_object_as
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import EmailStr

from app.server.config import config
from app.server.middlewares.token_validation import validate_token
from app.server.models.user import User, SignupData, Token
from app.server.repositories.user_repository import UserRepository

router = APIRouter()

user_rep_instance = UserRepository()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
logging.basicConfig(level=logging.INFO)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_repository() -> UserRepository:
    return user_rep_instance

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], user_rep = Depends(validate_token)) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except InvalidTokenError:
#         raise credentials_exception
#     user = await user_rep.get_user_by_name(username=username)
#     if user is None:
#         raise credentials_exception
#     return user


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

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)