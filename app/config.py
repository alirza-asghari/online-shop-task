import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str = "postgresql://alireza:password@localhost:5432/database"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", 5432))
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "database"

    # JWT configuration
    SECRET_KEY: str = 'secret'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class config:
        env_file = ".env"

config = Settings()
