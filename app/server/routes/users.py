from typing import Annotated, List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
import logging

from jwt import InvalidTokenError
from pydantic import BaseModel, EmailStr
from pymongo.errors import DuplicateKeyError

from app.server.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.server.config import config

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logging.basicConfig(level=logging.INFO)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await User.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(signup_data: SignupData):
    user_with_username = await User.find_one({"username": signup_data.username})
    if user_with_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    user_with_email = await User.find_one({"email": signup_data.email})
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
    await User.insert_one(user)
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(user: LoginData):
    try:
        logging.info("Attempting to find user by email")
        user_dict = await User.find_one({"email": user.email})
        if not user_dict:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if not verify_password(user.password, user_dict.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        logging.info(user_dict.id)
        access_token = create_access_token(data={"sub": user_dict.username})

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401)
@router.get("/", status_code=status.HTTP_200_OK)
async def read_user(current_user: Annotated[User, Depends(get_current_user)]):
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
