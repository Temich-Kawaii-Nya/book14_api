import logging

from fastapi import FastAPI

from fastapi import FastAPI

from .config.config import get_config
from .db.database import init_db
from .routes.books import router as book_router
from .routes.collections import router as collection_router
from .routes.quotes import router as quotes_router
from .routes.users import router as user_router

app = FastAPI()
cfg = get_config()
app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(book_router, tags=["Books"], prefix="/books")
app.include_router(collection_router, tags=["Collections"], prefix="/collections")
app.include_router(quotes_router, tags=["Quotes"], prefix="/quotes")



@app.on_event("startup")
async def startup():
    await init_db(cfg)

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    logging.info("loading root")
    return {"message": "Welcome to your beanie powered app!"}