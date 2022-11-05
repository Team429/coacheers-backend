from functools import lru_cache

from pydantic import BaseSettings


@lru_cache()
def get_env():
    settings = Settings()
    return settings


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str

    class Config:
        env_file = 'config/.env'
