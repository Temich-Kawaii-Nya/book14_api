import logging
from typing import Annotated

from beanie import init_beanie
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.server.config.config import Config, get_config
from app.server.models.user import User


async def init_db(cfg: Config):
    logging.info(cfg.DATABASE_URL)
    client = AsyncIOMotorClient(cfg.DATABASE_URL)
    await init_beanie(database=client[cfg.DATABASE_NAME], document_models=[User])
