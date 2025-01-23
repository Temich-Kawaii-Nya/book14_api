import logging
from datetime import timedelta, datetime
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from starlette import status

from ..config.config import Config, get_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

from ..models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
        data: dict,
        expires_delta: timedelta = None):
    logging.info("start creating token")
    to_encode = data.copy()
    cfg = get_config()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm="HS256")
    logging.info("token created")
    return encoded_jwt


def decode_access_token(token: str):
    cfg = get_config()
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def validate_token(
        token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cfg = get_config()
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms="HS256")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await User.find_one({"username": username})
    if user is None:
        raise credentials_exception
    return user