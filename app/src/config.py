import os
import secrets
from functools import lru_cache
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.dependencies import root_dir


def get_secret(secret_path: str):
    try:
        with open(f"{secret_path}", 'r') as fin:
            return fin.read()
    except FileNotFoundError:
        print(f"Error, secret '{secret_path}' not found!")
        raise

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(root_dir, '.env'))
    APP_NAME: str = "Inventory App"
    HOSTNAME: AnyHttpUrl
    SECRET_KEY: str = secrets.token_urlsafe()
    JWT_ALGO: str
    ACCESS_TOKEN_EXPIRE: int
    PWD_ALGO: str
    ACCESS_TOKEN_EXPIRE: int = 30
    POSTGRES_DB: str
    POSTGRES_SERVER: str
    PGPORT: int
    POSTGRES_USER: str
    POSTGRES_PWD: str = get_secret(os.getenv("POSTGRES_PWD"))
    BASE_ADMIN_PWD: str
    BASE_GUEST_PWD: str

    @field_validator("POSTGRES_PWD", mode="before")
    @classmethod
    def load_secret(cls, value):
        if value and os.path.exists(value):
            return get_secret(value)
        return value


@lru_cache()
def get_settings() -> Settings:
    return Settings()


