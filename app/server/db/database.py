from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.server.Config import Config
from app.server.models.book import Book
from app.server.models.collection import Collection
from app.server.models.description import Description
from app.server.models.quote import Quote
from app.server.models.user import User


async def init_db():
    client = AsyncIOMotorClient(Config.DATABASE_URL)
    await init_beanie(database=client[Config.DATABASE_NAME], document_models=[User, Book, Quote, Collection, Description])