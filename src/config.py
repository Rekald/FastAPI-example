import os
from functools import lru_cache
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.dependencies import source_dir


class Settings(BaseSettings):
    APP_NAME: str = "Inventory App"
    HOSTNAME: AnyHttpUrl
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BASE_ADMIN_PWD: str
    BASE_GUEST_PWD: str
    model_config = SettingsConfigDict(env_file=os.path.join(source_dir, '.env'))


@lru_cache()
def get_settings() -> Settings:
    return Settings(_env_file=os.path.join(source_dir, 'local.env'), _env_file_encoding='utf-8')
