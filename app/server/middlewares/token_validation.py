from fastapi import Request, HTTPException, middleware
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

from app.server.config import config

@middleware("http")
async def validate_token(request: Request, call_next):
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        payload = jwt.decode(token, config.SECRET_KEY, algorithms="HS256")
        request.state.user = payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    response = await call_next(request)
    return response