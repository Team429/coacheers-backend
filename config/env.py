from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_env():
    return Settings()
