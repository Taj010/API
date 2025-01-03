
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    SUPABASE_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    SUPABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
SUPABASE_URL = settings.SUPABASE_URL
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES