from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
@lru_cache
def get_config():
    return Config()
class Config(BaseSettings):
    DATABASE_URL: str
    DATABASE_NAME: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(env_file=".env")