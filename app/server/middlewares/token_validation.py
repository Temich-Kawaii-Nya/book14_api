from typing import Annotated

from fastapi import Request, HTTPException, middleware, Depends
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from app.server.config import config
from app.server.models.user import User


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
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