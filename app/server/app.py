from fastapi import FastAPI
from .db.database import init_db
from .routes.users import router
app = FastAPI()
app.include_router(router, tags=["Users"], prefix="/users")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Welcome to your beanie powered app!"}