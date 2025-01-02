from fastapi import FastAPI

from .db.database import init_db
from .routes.users import router as user_router
from .routes.books import router as book_router

app = FastAPI()
app.include_router(user_router, tags=["Users"], prefix="/users")
app.include_router(book_router, tags=["Books"], prefix="/books")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}